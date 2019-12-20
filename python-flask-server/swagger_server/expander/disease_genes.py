
from swagger_server.models.transformer_info import TransformerInfo
from swagger_server.models.parameter import Parameter
from swagger_server.models.transformer_query import TransformerQuery
from swagger_server.models.gene_info import GeneInfo
from swagger_server.models.gene_info_identifiers import GeneInfoIdentifiers
from swagger_server.models.attribute import Attribute

import requests
from ncats.translator.modules.disease.gene.disease_associated_genes import DiseaseAssociatedGeneSet

import json

transformer_name = 'MONDO disease association'
valid_controls = ['disease_id']
control_names = {'disease_id': 'disease ID'}


def expander_info():
    """
        Return information for this expander
    """
    global transformer_name, control_names

    with open("transformer_info.json",'r') as f:
        info = TransformerInfo.from_dict(json.loads(f.read()))
        transformer_name = info.name
        control_names = dict((name,parameter.name) for name, parameter in zip(valid_controls, info.parameters))
        return info


def expand(query: TransformerQuery):
    """
        Execute this expander, find all genes correlated to query genes.
    """
    controls = {control.name:control.value for control in query.controls}
    genes = {}
    if control_names['disease_id'] not in controls:
        msg = "required parameter '{}' not specified".format(control_names['disease_id'])
        return ({ "status": 400, "title": "Bad Request", "detail": msg, "type": "about:blank" }, 400 )

    dags = DiseaseAssociatedGeneSet(controls[control_names['disease_id']], query_biolink=False)
    # results are a dataframe
    results = dags.results.to_dict('records')

    for result in results:

        gene_id = result['hit_id']
        symbol = result['hit_symbol']
        relation = result['relation']
        sources = result['sources']

        gene = GeneInfo(gene_id=gene_id,
                        identifiers=GeneInfoIdentifiers(hgnc=gene_id),
                        source=transformer_name,
                        attributes=[
                            Attribute(
                                name='gene_symbol',
                                value=str(symbol),
                                source=transformer_name
                            ),
                            Attribute(
                                name='relation',
                                value=str(relation),
                                source=str(sources)
                            )
                        ])
        genes[gene_id] = gene

    return list(genes.values())


expander_info()

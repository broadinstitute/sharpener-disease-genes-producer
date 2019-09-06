
from swagger_server.models.transformer_info import TransformerInfo
from swagger_server.models.parameter import Parameter
from swagger_server.models.transformer_query import TransformerQuery
from swagger_server.models.gene_info import GeneInfo
from swagger_server.models.gene_info_identifiers import GeneInfoIdentifiers
from swagger_server.models.attribute import Attribute

import requests
from translator_modules.disease.gene.disease_associated_genes import DiseaseAssociatedGeneSet

def expander_info():
    """
        Return information for this expander
    """
    return TransformerInfo(
        name='Disease Association from MONDO ID',
        function='producer',
        description='Gene-list expander based on disease-specific genes',
        parameters=[
            Parameter(
                name='Disease ID',
                type='string',
                default='MONDO:0005015'
            )
        ],
        required_attributes = []
    )


def expand(query: TransformerQuery):
    """
        Execute this expander, find all genes correlated to query genes.
    """
    controls = {control.name:control.value for control in query.controls}
    genes = {}

    dags = DiseaseAssociatedGeneSet(controls['Disease ID'], query_biolink=False)
    # results are a dataframe
    results = dags.results.to_dict('records')

    for result in results:

        gene_id = result['hit_id']
        symbol = result['hit_symbol']
        relation = result['relation']
        sources = result['sources']

        gene = GeneInfo(gene_id=gene_id,
                        identifiers=GeneInfoIdentifiers(hgnc=gene_id),
                        attributes=[
                            Attribute(
                                name='gene_symbol',
                                value=str(symbol),
                                source='Disease Association from MONDO ID'
                            ),
                            Attribute(
                                name='relation',
                                value=str(relation),
                                source=str(sources)
                            )
                        ])
        genes[gene_id] = gene

    return list(genes.values())

# CORR_URL = 'https://indigo.ncats.io/gene_knockout_correlation/correlations/{}'


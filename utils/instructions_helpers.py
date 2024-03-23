from elasticsearch import Elasticsearch

def get_instructions(es_hosts, api_key):

    """
    Fetches documents from an Elasticsearch index where the status field is not 'not ok',
    returning only the 'instruction' part of each document.
    
    Parameters:
    - es_hosts (list): A list of host URLs for the Elasticsearch cluster.
    - api_key (str): The API key used for authenticating with the Elasticsearch cluster.
    
    Returns:
    - list: A list of 'instruction' fields from the fetched documents.
    """

    es = Elasticsearch(es_hosts, api_key=api_key)

    page = es.search(
        index='instructions',
        scroll='5m',  
        size=10000,  
        query={
            "bool": {
                "must_not": {
                    "match": {
                        "status": "not ok"
                    }
                }
            }
        }
    )


    scroll_id = page['_scroll_id']
    all_instructions = [hit['_source']['instruction'] for hit in page['hits']['hits']]

    while len(page['hits']['hits']):
        page = es.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = page['_scroll_id']
        all_instructions.extend(hit['_source']['instruction'] for hit in page['hits']['hits'])

    es.clear_scroll(scroll_id=scroll_id)
    
    return all_instructions

import elasticsearch
from drinking_pleasure.my_settings import ES


class MakeESQuery:
    def __init__(self,
                 search_query=None,  # str
                 recipe_name=None,  # str
                 price=None,  # [0, 5000]
                 tag=None,  # list
                 large_category=None,  # str
                 medium_category=None,  # str
                 small_category=None):  # str

        self.base_query = {
            "query": {
                "bool": {
                    "must": [],
                    "should": [],
                    "filter": [],
                    "must_not": [],
                }
            }
        }
        self.search_query = search_query
        self.recipe_name = recipe_name
        self.price = price
        self.tag = tag
        self.large_category = large_category
        self.medium_category = medium_category
        self.small_category = small_category
        self.query = self.make_query()

    def es_conn():
        try:
            cluster = ES['es_address'].values()
            print(cluster, ES['es_port'])
            es_client = elasticsearch.Elasticsearch(
                hosts=cluster,
                port=ES['es_port'],
                timeout=60,
                max_retries=3,
                basic_auth=(ES['id'], ES['pw']),
            )

            return es_client
        except Exception as ex:
            print("ES CONNECTION ERROR : {}".format(ex))

            return None

    def add_search_query(self, query):
        query["query"]["bool"]["should"].append({
            "query_string": {
                "query": self.search_query,
                "fields": [
                    "recipe_name^2.0",
                    "main_meterial.drink_name^1.0",
                    "sub_meterial.meterial_name^1.0",
                ]
            }
        })
        query["query"]["bool"]["filter"].append({
          "nested": {
            "path": "tag_list",
            "query": {
              "bool": {
                "filter": [
                  {
                    "term": {
                      "tag_list.tags": self.search_query
                    }
                  }
                ]
              }
            }
          }
        })
        return query

    def add_recipe_name(self, query):
        query["query"]["bool"]["must"].append({
            "match": {
                "recipe_name": self.recipe_name
            }
        })
        return query

    def add_price(self, query):
        query["query"]["bool"]["must"].append({
            "range": {
                ""
            }
        })
        return query

    def add_tag(self, query):
        query["query"]["bool"]["filter"].append({
          "nested": {
            "path": "tag_list",
            "query": {
              "bool": {
                "filter": [
                  {
                    "term": {
                      "tag_list.tags": self.tag
                    }
                  }
                ]
              }
            }
          }
        })
        return query

    def add_large_category(self, query):
        query["query"]["bool"]["filter"].append({
            "term": {
                "main_meterial.large_category": self.large_category
            }
        })
        return query

    def add_medium_category(self, query):
        query["query"]["bool"]["filter"].append({
            "term": {
                "main_meterial.medium_category": self.medium_category
            }
        })
        return query

    def add_small_category(self, query):
        query["query"]["bool"]["filter"].append({
            "term": {
                "main_meterial.small_category": self.small_category
            }
        })

    def make_query(self):
        """
        """
        query = self.base_query
        if self.search_query:
            query = self.add_search_query(query)
        if self.recipe_name:
            query = self.add_recipe_name(query)
        if self.price:
            query = self.price(query)
        if self.tag:
            query = self.add_tag(query)
        if self.large_category:
            query = self.add_large_category(query)
        if self.medium_category:
            query = self.add_medium_category(query)
        if self.small_category:
            query = self.add_small_category(query)

    def get_query(self):
        return self.query

    def run_query(self, index):
        my_res = []
        es_client = self.es_conn()

        res = es_client.search(index=index, body=self.query, request_timeout=60)
        for r in res['hits']['hits']:
            my_res.append(r['_source'])

        return my_res


if __name__ == '__main__':
    es = MakeESQuery()
    print(es.get_query())

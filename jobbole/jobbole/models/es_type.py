from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=['localhost'])

class CustomCustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomCustomAnalyzer("ik_max_word", filter=["lowercase"])

class JobboleItemType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    url = Keyword()
    url_obj_id = Keyword()
    title = Text(analyzer="ik_max_word")
    create_time = Date()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = 'jobbole'
        doc_type = 'article'

if __name__ == '__main__':
    JobboleItemType.init()
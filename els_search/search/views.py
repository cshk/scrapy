from django.shortcuts import render
from django.views.generic.base import View
from search.models import JobboleItemType
from django.http import HttpResponse
import json
from elasticsearch import  Elasticsearch
from datetime import datetime


client = Elasticsearch(hosts=['localhost'])

# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        datas = []
        if key_words:
            s = JobboleItemType.search()
            s = s.suggest('my_suggest', key_words, completion={
                'field':"suggest",
                'fuzzy':{
                    'fuzziness':2,
                },
                "size":10,
            })
            suggestion = s.execute_suggest()
            for m in suggestion.my_suggest[0].options:
                source = m._source
                datas.append(source['title'])
        return HttpResponse(json.dumps(datas), content_type="application/json")

class SearchView(View):
    def get(self, request):
        key_words = request.GET.get('q', '')
        page = request.GET.get('p',"1")
        try:
            page = int(page)
        except:
            page = 1
        start_time = datetime.now()
        response = client.search(
            index='jobbole',
            body={
                "query":{
                    "multi_match":{
                        "query":key_words,
                        "fields":["tags", "title", "content"]
                    }
                },
                "from":(page-1)*10,
                "size":10,
                "highlight":{
                    "pre_tags": ["<span class='keyWord'>"],
                    "post_tags": ["</span>"],
                    "fields":{
                        "title":{},
                        "content":{},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time-start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page%10) > 0:
            page_nums = int(total_nums/10+1)
        else:
            page_nums = int(total_nums/10)
        hit_lst = []
        for hit in response['hits']["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict['title'] = "".join(hit["highlight"]["title"])
            else:
                hit_dict['title'] = hit["_source"]["title"]

            if "content" in hit["highlight"]:
                hit_dict['content'] = "".join(hit["highlight"]["content"])[:500]
            else:
                hit_dict['content'] = hit["_source"]["content"][:500]
            hit_dict['create_time'] = hit["_source"]["create_time"]
            hit_dict['url'] = hit["_source"]["url"]
            hit_dict['score'] = hit["_score"]
            hit_lst.append(hit_dict)
        return render(request, "result.html", {"page":page,
                                               "all_hits":hit_lst,
                                               "key_words":key_words,
                                               "total_nums":total_nums,
                                               "page_nums":page_nums,
                                               "last_seconds":last_seconds})


#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo 
from ac_trie import Trie 
import pongoclient
import json


tagsParser = Trie('./dict/skill.txt')

conn = pymongo.Connection(host='192.168.4.216', port=19753) 
article = conn.tags.article 
def cut(value):
    value=value.lower().replace('&nbsp','')
    value = value.encode('UTF-8')
    terms = tagsParser.parse(value)
    v = {}
    for i in terms:
        v[i[0]]=i[1]
    return v.values()
def ad_query(k):
    request='{ "action" : "searchJob" , "q" : { "keyword" : "'+k+'"} , "sort" : 1 , "output" : { "format" : "json" , "offset" : 0 , "size" : 10}}'
    return pongoclient.send_request('search',request)
    

def load_data(): 
    blog_id_f = open('/home/pongo/gitwork/file_bak/data/blog_id.txt') 
    for id in blog_id_f:
        id=id.strip()
        one = article.find_one({"_id": id}, {"Title": 1,"Description":1,"category":1,'UserName':1})
        text=one["Title"]+one["Description"]+one["category"] 
        url = 'http://blog.csdn.net/'+one["UserName"]+'/article/details/'+str(id)
        terms = cut(text)
        if len(terms)>0:
#            print '=============='
#            print text
            print url,'\t',','.join(set(terms))
#            k = " ".join(set(terms))
#            data = ad_query(k)
#            jdata = json.loads(data.replace("''","0"),strict=False)
#            if jdata["totalCount"] >0 :
#                items = jdata["items"]
#                out = ''
#                for t in items:
#                    out +=str(t['jobId'])+" "+t['jobTitle']+" "
#                print out


if __name__ == '__main__':
    load_data()



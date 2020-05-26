import pandas as pd
from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View
import geopandas as geopd
def get_aus_geo():
    url = 'https://raw.githubusercontent.com/infinite1/ccc-ass2/master/demo_website'
    aus_geo = f'{url}/australian-states.json'
    aus=geopd.read_file(aus_geo)
    aus['STATE_CODE']=aus['STATE_CODE'].astype(int)
    return aus

class CouchClient:
    def __init__(self,admin,password,url,db_name):
        '''
        admin:admin
        password:admin
        url:'http://127.0.0.1:5984'
        '''
        self.admin=admin
        self.password=password
        self.url=url
        self.db_name=db_name
        self.client=None
        self.db=None
    def connect_db(self):
        self.client = CouchDB(self.admin, self.password, url=self.url, connect=True)
        self.db=self.client[self.db_name]
    def get_tweets(self):
        selector_pos = {"sentiment": {"polarity": {"$gt": 0 }}}
        docs_pos = self.db.get_query_result(selector_pos,raw_result=True, limit=1000)

        selector_neg = {"sentiment": {"polarity": {"$lt": 0 }}}
        docs_neg = self.db.get_query_result(selector_neg,raw_result=True, limit=1000)
        return docs_pos['docs'],docs_neg['docs']
    def get_city_tweets_count(self,doc_id,view_name,label):
        
        map_function='''
            function (doc) {
                var place=doc.place.full_name.split(",");
                if (doc.sentiment.polarity>0){
                    emit([place[0],"pos"], 1);
                }
                if (doc.sentiment.polarity<0){
                    emit([place[0],"neg"], 1);
                }
                
            }
        '''
        ddoc = DesignDocument(self.db, document_id=doc_id)
        ddoc.add_view(view_name,map_function,reduce_func="_sum")
        ddoc.save()
        
        cities=['Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Sydney']
        result = self.db.get_view_result('_design/'+doc_id, view_name,group_level=2,raw_result=True)
        city_stat=dict()
        for item in result['rows']:
            city=item['key'][0]
            if not city or city not in cities: continue
            data_label=item['key'][1]
            if data_label==label :
                city_stat[city]=item['value']
        tweets_count=[city_stat.get(city,0) for city in city_stat]
        return tweets_count
    def get_state_tweets_count(self,doc_id,view_name,label):
        '''
        db_name:"tweet"
        doc_id_:'view'
        view_name:'myview'
        label:pos or neg
        '''
        try:
            map_function='''
                function (doc) {
                    var place=doc.place.full_name.split(",");
                    if (doc.sentiment.polarity>0){
                        emit([place[1],"pos"], 1);
                    }
                    else {
                        emit([place[1],"neg"], 1);
                    }
                    
                }
            '''
            ddoc = DesignDocument(self.db, document_id='view')
            ddoc.add_view('myview',map_function,reduce_func="_sum")
            ddoc.save()
        except:
            pass
        result = self.db.get_view_result('_design/'+doc_id, view_name,group_level=2,raw_result=True)
        state_stat=dict()
        state_code=[
            "New South Wales",
            "Victoria",
            "Queensland",
            "South Australia",
            "Western Australia",
            "Tasmania",
            "Northern Territory",
        ]
        for item in result['rows']:
            state=item['key'][0]
            if not state: continue
            state=state.strip()
            data_label=item['key'][1]
            if data_label==label and state in state_code:
                state_stat[state]=item['value']
        
        state_count=[ state_stat.get(state,0) for state in state_code]
        return state_code,state_count
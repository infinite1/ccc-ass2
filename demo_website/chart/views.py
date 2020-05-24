from django.shortcuts import render
from django.views.generic import TemplateView
from .module.data_collector import CouchClient
import pandas as pd
def chart_view(request):
    #get tweets count and state name
    db_client=CouchClient("admin","admin",'http://127.0.0.1:5984','tweet')
    db_client.connect_db()
    state,tweets=db_client.get_state_tweets_count("view","myview","neg")
    #get job lass rate data
    url = 'https://raw.githubusercontent.com/infinite1/ccc-ass2/master/demo_website'
    unemployment_url = f'{url}/aus_job_data.csv'
    unemployment_data=pd.read_csv(unemployment_url)
    unemployment_rate=unemployment_data['Job Loss Rate'].tolist()
    
    context={"state":state,"tweets":tweets,"unemployment_rate":unemployment_rate}
    return render(request,"chart/base.html",context)


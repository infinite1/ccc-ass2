from django.shortcuts import render
from django.views.generic import TemplateView
from .module.data_collector import CouchClient
import pandas as pd
def chart_view(request):
    #get tweets count and state name
    db_client=CouchClient("admin","password",'http://127.0.0.1:5984','tweets')
    # db_client=CouchClient("admin","admin",'http://127.0.0.1:5984','tweet')
    db_client.connect_db()
    cur_neg_tweets=db_client.get_city_tweets_count("views","city","neg")
    # get job lass rate data
    url = 'https://raw.githubusercontent.com/infinite1/ccc-ass2/master/demo_website'
    unemployment_url = f'{url}/aus_job_data.csv'
    unemployment_data = pd.read_csv(unemployment_url)
    unemployment_rate = unemployment_data['Job Loss Rate'].tolist()
    city_unemployment_rate=[unemployment_rate[1],unemployment_rate[2],unemployment_rate[4],unemployment_rate[3],unemployment_rate[0]]
    # get homeless data
    homeless_url = f'{url}/aus_homeless_data.csv'
    homeless_data = pd.read_csv(homeless_url)
    homeless_count = homeless_data['Homeless'].tolist()
    # get health data
    health_url=f'{url}/aus_health_data.csv'
    health_data=pd.read_csv(health_url)
    health_rate=health_data['Health_And_Wellbeing'].tolist()
    #combine homeless,health,job less
    bubble=[]
    for i in range(len(health_rate)):
        x,y,r=health_rate[i],homeless_count[i],unemployment_rate[i]
        bubble.append({"x":x,"y":y,"r":r})
    #get city data
    city_url=f'{url}/aus_city_tweets.csv'
    city_data=pd.read_csv(city_url)
    city_tweets=city_data['Negative'].tolist()
    #state
    state=[
            "New South Wales",
            "Victoria",
            "Queensland",
            "South Australia",
            "Western Australia",
            "Tasmania",
            "Northern Territory",
        ]
    context = {"cur_neg_tweets": cur_neg_tweets,
               "unemployment_rate": city_unemployment_rate,
               "homeless_count":homeless_count,
               "health":health_rate,
               "city_tweets":city_tweets,
               "state":state}
    return render(request, "chart/base.html", context)


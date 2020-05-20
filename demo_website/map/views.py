from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import folium
from folium.plugins import BeautifyIcon
import geopandas as geopd
import pandas as pd
import json
import couchdb
from django.views.generic import TemplateView
def home_view(request):
    return render(request,"map/home.html")

class FoliumView(TemplateView):
    template_name = "map/folium.html"
    def get_tweets(self):
        couchdb_url='http://admin:password@127.0.0.1:5984/'
        db=couchdb.Server(couchdb_url)
        tweet_db=db['tweets']
        mango={"selector": {"coordinates": {"$gt": [-1000,-1000]}}}
        results = tweet_db.find(mango)
        return results

    def add_tweets_on_map(self):
        fg_positive=folium.FeatureGroup(name='Positive tweets', show=False)
        fg_negtive=folium.FeatureGroup(name='Negtive tweets', show=False)
        # add streeming tweets into map
        tweets=self.get_tweets()
        if tweets:
            for tweet in tweets:
                try:
                    if tweet['sentiment']["polarity"]>0:
                        folium.Marker(
                            location=[tweet['coordinates'][1],tweet['coordinates'][0]],
                            popup=tweet['text'],
                            icon=BeautifyIcon(icon='thumbs-up',background_color='#99CCFF',border_color='transparent')
                        ).add_to(fg_positive)
                    else:
                        folium.Marker(
                            location=[tweet['coordinates'][1],tweet['coordinates'][0]],
                            popup=tweet['text'],
                            icon=BeautifyIcon(icon='thumbs-down',background_color='#FF9999',border_color='transparent')
                        ).add_to(fg_negtive)
                except:
                    pass
        return fg_positive,fg_negtive
    def interactive_map(self,data):
        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        NIL = folium.features.GeoJson(
            data,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['STATE_NAME','Job Loss Rate'],
                aliases=['STATE: ','Unemployment Rate %: '],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        return NIL
    def get_context_data(self, **kwargs):
        url = 'https://raw.githubusercontent.com/infinite1/ccc-ass2/master/demo_website'
        aus_geo = f'{url}/australian-states.json'
        aus_unemployment = f'{url}/aus_job_data.csv'
        aus_data = pd.read_csv(aus_unemployment)
        aus=geopd.read_file(aus_geo)
        aus['STATE_CODE']=aus['STATE_CODE'].astype(int)
        aus=aus.merge(aus_data,on="STATE_CODE")

        
        figure = folium.Figure()
        m = folium.Map(
            location=[-27.81, 164.96],
            zoom_start=4,
        )
        m.add_to(figure)
        #color by job loss rate  
        folium.Choropleth(
            geo_data=aus,
            name='Unemployment in State',
            data=aus_data,
            columns=['STATE_CODE','Job Loss Rate'],
            key_on="feature.properties.STATE_CODE",
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='2018 Unemployment Rate (%)',
            smooth_factor=0
        ).add_to(m)
        NIL=self.interactive_map(aus)
        m.add_child(NIL)
        m.keep_in_front(NIL)
        #add feature group in layer control
        fg_positive,fg_negtive=self.add_tweets_on_map()
        m.add_child(fg_positive)
        m.add_child(fg_negtive)
        folium.LayerControl().add_to(m)
        
        figure.render()
        
        return {"map": figure}


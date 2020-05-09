from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import folium
import geopandas as geopd
import pandas as pd
import json
import couchdb
from django.views.generic import TemplateView
def DefaultView(request):
    tk='pk.eyJ1Ijoiamx1bzEiLCJhIjoiY2s5ZTJib2UxMDA0dTNtdGozbjI1amxoaiJ9.SGvgK0GJLR38F7T8ihRxHw'
    return render(request,'map/default.html',{'mapbox_access_token':tk})

def LeafletView(request):
    tk='pk.eyJ1Ijoiamx1bzEiLCJhIjoiY2s5ZTJib2UxMDA0dTNtdGozbjI1amxoaiJ9.SGvgK0GJLR38F7T8ihRxHw'
    return render(request,'map/leaflet.html',{'mapbox_access_token':tk})


class FoliumView(TemplateView):
    template_name = "map/folium.html"
    def get_tweets(self):
        couchdb_url='http://admin:admin@127.0.0.1:5984/'
        db=couchdb.Server(couchdb_url)
        tweet_db=db['tweets']
        mango={"selector": {"coordinates": {"$gt": [-1000,-1000]}}}
        results = tweet_db.find(mango)
        return results

    def get_context_data(self, **kwargs):
        #figure = folium.Figure()
        
        url = 'https://raw.githubusercontent.com/infinite1/ccc-ass2/master/demo_website'
        aus_geo = f'{url}/australian-states.json'
        aus_unemployment = f'{url}/aus_data.csv'
        aus_data = pd.read_csv(aus_unemployment)
        aus=geopd.read_file(aus_geo)
        aus['STATE_CODE']=aus['STATE_CODE'].astype(int)
        aus=aus.merge(aus_data,on="STATE_CODE")
        
        # m = folium.Map(location=[-27.81, 134.96],zoom_start=5)
        
        #m.add_to(figure)

        figure = folium.Figure()
        m = folium.Map(
            location=[-27.81, 134.96],
            zoom_start=4,
        )
        #add streeming tweets into map
        tweets=self.get_tweets()
        if tweets:
            for tweet in tweets:
                folium.Marker(
                    location=[tweet['coordinates']['coordinates'][1],tweet['coordinates']['coordinates'][0]],
                    popup=tweet['text'],
                    icon=folium.Icon(icon='cloud')
                ).add_to(m)
        
        m.add_to(figure)
    
        folium.Choropleth(
            geo_data=aus,
            name='Unemployment in State',
            data=aus_data,
            columns=['STATE_CODE','Job Loss Rate'],
            key_on="feature.properties.STATE_CODE",
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Unemployment Rate (%)',
            smooth_factor=0
        ).add_to(m)
        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        NIL = folium.features.GeoJson(
            aus,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['STATE_NAME','Job Loss Rate'],
                aliases=['STATE: ','Unemployment Rate %: '],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        m.add_child(NIL)
        m.keep_in_front(NIL)
        folium.LayerControl().add_to(m)
        figure.render()
        
        return {"map": figure}


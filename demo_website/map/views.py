from django.shortcuts import  render
from django.views.generic import TemplateView
import folium
from folium.plugins import BeautifyIcon
from folium.plugins import MarkerCluster
import geopandas as geopd
import pandas as pd
import json
import couchdb
from cloudant.client import CouchDB
from .module.data_collector import CouchClient
from .module.data_collector import get_aus_geo
def home_view(request):
    return render(request,"map/base.html")

class FoliumView(TemplateView):
    template_name = "map/folium.html"   
    def add_tweets_on_map(self,db_client):
        # fg_positive=folium.FeatureGroup(name='Positive tweets', show=True)
        # fg_negtive=folium.FeatureGroup(name='Negtive tweets', show=True)
        positive_marker_cluster=MarkerCluster(name="Positive Tweets Cluster")
        negtive_marker_cluster=MarkerCluster(name="Negtive Tweets Cluster")
        # retrive tweets data
        tweets_pos,tweets_neg=db_client.get_tweets()
        for tweet in tweets_pos:
            try:

                marker=folium.Marker(
                                location=[tweet['coordinates'][1],tweet['coordinates'][0]],
                                popup=tweet['text'],
                                icon=BeautifyIcon(icon='thumbs-up',background_color='#99CCFF',border_color='transparent')
                            )
                positive_marker_cluster.add_child(marker)
            except:
                pass
        for tweet in tweets_neg:
            try:
                marker=folium.Marker(
                                location=[tweet['coordinates'][1],tweet['coordinates'][0]],
                                popup=tweet['text'],
                                icon=BeautifyIcon(icon='thumbs-down',background_color='#FF9999',border_color='transparent')
                            )
                negtive_marker_cluster.add_child(marker)
            except:
                pass
        return positive_marker_cluster,negtive_marker_cluster
        
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
                aliases=['STATE: ','Total Negative Tweets: '],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        return NIL
    def get_context_data(self, **kwargs):
        db_client=CouchClient("admin","password",'http://127.0.0.1:5984','tweets')
        db_client.connect_db()
        aus_data=db_client.basemap_stat("view","myview","neg")
        aus=get_aus_geo()
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
            legend_name='Negtive Tweets Count ',
            smooth_factor=0
        ).add_to(m)
        #interactive map
        NIL=self.interactive_map(aus)
        m.add_child(NIL)
        m.keep_in_front(NIL)
        #add cluster in layer control
        positive_marker_cluster,negtive_marker_cluster=self.add_tweets_on_map(db_client)
        m.add_child(positive_marker_cluster)
        m.add_child(negtive_marker_cluster)
        
        folium.LayerControl().add_to(m)
        
        figure.render()
        
        return {"map": figure}


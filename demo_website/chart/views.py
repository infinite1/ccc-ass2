from django.shortcuts import render
from django.views.generic import TemplateView
from .module.data_collector import CouchClient
from .module.data_collector import get_aus_geo

def chart_view(request):
    db_client=CouchClient("admin","admin",'http://127.0.0.1:5984','tweet')
    db_client.connect_db()
    state,tweets=db_client.get_state_tweets_count("view","myview","neg")
    context={"state":state,"tweets":tweets}
    return render(request,"chart/base.html",context)

# Create your views here.
class DataVisualization(TemplateView):
    template_name = "chart/chart.html"
    def get_context_data(self, **kwargs):
        
        return {"state_tweets_count":[100,100,200,300]}


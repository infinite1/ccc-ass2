from django.urls import path
from . import views
app_name = 'map'
urlpatterns = [
    path('', views.DefaultView, name='default'),
    path('leaflet/', views.LeafletView, name='leaflet'),
    path('folium/', views.FoliumView.as_view(), name='folium')
]
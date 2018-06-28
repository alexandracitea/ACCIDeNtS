from django.urls import path
from . import views

urlpatterns = [
    #/map/
    path('', views.index, name='index'),

    #/map/accidents
    path('accidents/', views.splitAccidents, name='accidents'),

    # /map/id
    path('accidents/<incident_id>/', views.detail, name='detail')
]

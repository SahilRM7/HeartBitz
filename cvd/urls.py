from django.urls import path
from . import views

urlpatterns = [
    path('cvd/', views.predict, name='cvd'),
    path('result/', views.attribute_pie_chart, name='rst')
]

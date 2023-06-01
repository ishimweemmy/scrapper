from django.urls import path
from . import views

urlpatterns = [
    path('constative', views.scrapeposts)
]

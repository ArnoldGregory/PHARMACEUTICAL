from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # Your other URL patterns go here
]



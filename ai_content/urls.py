from django.urls import path
from . import views
urlpatterns = [
    path('', views.youtube, name='youtube'),
    path('content/<str:title>/<str:channel>/<str:id>',views.content, name='content')
]

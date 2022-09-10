from django.urls import path
from livestream import views


urlpatterns = [
    #トップページ
    path('', views.index, name='index'),

    #ラップトップカメラにアクセスします
    path('video/', views.video_feed, name="video_feed"),
]
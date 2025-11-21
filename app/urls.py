from django.urls import path
from . import views, api_views

urlpatterns = [
    # ===== Web 页面路由 =====
    path('', views.index, name='index'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),

    # ===== API 路由（只读，安全） =====
    path('api/articles/', api_views.api_article_list, name='api_article_list'),
    path('api/articles/<int:pk>/', api_views.api_article_detail, name='api_article_detail'),
    path('api/about/', api_views.api_about_info, name='api_about_info'),
]


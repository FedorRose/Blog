from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:cat_slug>/', views.HomeCat.as_view(), name='cat'),
    path('<slug:cat_slug>/<slug:post_slug>/', views.ShowPost.as_view(), name='single'),

]

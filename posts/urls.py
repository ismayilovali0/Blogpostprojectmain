from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.post_list, name='post_list'),
    
    # Post ddetail
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # Like, Favourite, Comment
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # About 
    path('about/', views.about_view, name='about'),

    #Tag
    path('tags/', views.tags_list, name='tags_list'),
    path('tags/<int:tag_id>/', views.tag_posts, name='tag_posts'),
]

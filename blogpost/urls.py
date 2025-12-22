from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import (
    homepage, post, about, search, postlist, allposts,
    post_detail, toggle_like, toggle_favourite, add_comment, about_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('post/<slug>/', post, name='post'),
    path('about/', about_view, name='about'),
    path('search/', search, name='search'),
    path('postlist/<slug>/', postlist, name='postlist'), 
    path('posts/', allposts, name='allposts'),
    path('post/<int:pk>/detail/', post_detail, name='post_detail'),
    path('post/<int:pk>/like/', toggle_like, name='toggle_like'),
    path('post/<int:pk>/favourite/', toggle_favourite, name='toggle_favourite'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
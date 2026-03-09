from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/<str:action>/', views.like_post, name='like_post'),  # action = 'like' или 'dislike'
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]

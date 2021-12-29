from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('blogs/',views.BlogListView.as_view(),name='blogs-all'),
    path('blog/<int:pk>',views.BlogDetailView.as_view(),name='blog-detail'),
    path('bloggers/',views.BlogAuthorListView.as_view(),name='bloggers-all'),
    path('blogger/<int:pk>',views.BlogAuthorDetailView.as_view(),name='blogs-by-author'),
    path('blog/<int:pk>/comment/',views.create_comment_blog,name='create-comment-blog')
]
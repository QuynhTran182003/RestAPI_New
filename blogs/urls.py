from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('api/blog/', views.blogs, name='blogs'),
    path('api/blog/blogId/<int:id>', views.blogId, name='blog_id'),
]
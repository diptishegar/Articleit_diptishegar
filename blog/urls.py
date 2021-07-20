from django.urls import path
from blog.views import (
	create_blog_view,
	account_view,
    home_view,
    detail_blog_view,
    edit_blog_view,
    delete_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('your_articles/', account_view, name="your_articles"),
    path('dashboard/', home_view, name="dashboard"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit/', edit_blog_view, name="edit"),
    path('<slug>/delete/', delete_view, name="delete"),
 ]
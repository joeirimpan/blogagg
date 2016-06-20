from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.articles_list, name="articles_list"),
	url(r'^blogs/new',views.new_blog, name="blog_new"),
	url(r'^blogs/',views.blogs_list, name="blogs_list"),
]
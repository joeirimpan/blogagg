import requests
import simplejson as json
import datetime  # noqa

from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render

from models import Article, Blog
from forms import BlogForm

TEST_API_KEY = 'YOUR_API_KEY_HERE'
BASE_URL = 'https://api.tumblr.com/v2/blog/%s.tumblr.com/posts/text?api_key=%s'


# Create your views here.
def articles_list(request):
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        articles = paginator.page(page)
    except(EmptyPage, InvalidPage):  # noqa
        articles = paginator.page(paginator.num_pages)
    return render(request, "articles_list.html", {"articles": articles})


def blogs_list(request):
    blogs = Blog.objects.all()
    return render(request, "blogs_list.html", {"blogs": blogs})


def new_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            _blog = form.save(commit=False)
            req_url = BASE_URL % (_blog.name, TEST_API_KEY)
            # parse json
            req = requests.get(req_url)
            jsonlist = json.loads(req.content)
            response = jsonlist['response']
            posts = response['posts']
            blog = response['blog']
            # for post in posts:
            # 	print post['body']

            _blog.title = blog['title']
            _blog.url = blog['url']
            _blog.save()

            for post in posts:
                article = Article()
                article.title = post['title']
                article.url = post['post_url']
                article.description = post['body']
                # article.published_date =
                # datetime.datetime.fromtimestamp(float(post['timestamp']))
                # print article.published_date
                article.blog = _blog
                article.save()
            return redirect('blogs.views.articles_list')
    else:
        form = BlogForm()
    return render(request, "new_blog.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404
from blog.models import BlogPost
from account.models import Account
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from django.http import HttpResponse
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

BLOG_POSTS_PER_PAGE = 10

def home_view(request):
	context ={}
	blog_posts = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts


	return render(request, "dashboard.html", context)

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
		return redirect('blog:dashboard')

	context['form'] = form

	return render(request, "blog/create_blog.html", context)

def dash_artices(request):
	context = {}
	if not request.user.is_authenticated:
			return redirect("login")
	blog_posts = BlogPost.objects.order_by('date_published')
	context['blog_posts'] = blog_posts

	return render(request, "dashboard.html", context)

def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "blog/your_articles.html", context)

def detail_blog_view(request, slug):

	context = {}
	
	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)

def delete_view(request, slug):
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")
	blog_post = get_object_or_404(BlogPost, slug=slug)
	if blog_post.author == user:
		blog_post.delete()
	else:
		return HttpResponse('You are not the author of that post.')
	return redirect ('blog:your_articles')


def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
			return redirect('blog:your_articles')
			

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)


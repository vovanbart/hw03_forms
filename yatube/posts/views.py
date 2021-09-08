from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    title = f'Записи сообщества <{group}>'
    context = {
        'group': group,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=author).count()
    post_list = Post.objects.order_by("-pub_date").filter(author=author)
    paginator = Paginator(post_list, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'post_count': post_count,
        'paginator': paginator,
        'author': author,
        'page_obj': page_obj, }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_count = Post.objects.count()
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post_count': post_count,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, post_id, is_edit=True):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {'form': form, 'is_edit': is_edit, 'post': post}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', user=User.username)
    return render(request, 'posts/create_post.html', {'form': form})

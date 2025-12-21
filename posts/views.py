from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Post, Author, Like, Favourite, Comment, About, Tag



def get_author(user):
    """Get author object for a user"""
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def homepage(request):
    """Homepage view with featured posts, latest posts and categories"""
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    
    context = {
        'object_list': featured,
        'latest': latest,
        'categories': categories,
    }
    return render(request, 'homepage.html', context)


def post(request, slug):
    """Single post view with interactions"""
    post = get_object_or_404(Post, slug=slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    
    # Increment view count
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Check like/favourite status
    is_liked = False
    is_favourited = False
    
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
        is_favourited = Favourite.objects.filter(user=request.user, post=post).exists()
    
    # Get comments
    comments = post.comments.all().order_by('-created_at')
    
    context = {
        'post': post,
        'latest': latest,
        'is_liked': is_liked,
        'is_favourited': is_favourited,
        'like_count': post.like_set.count(),
        'favourite_count': post.favourite_set.count(),
        'comments': comments,
    }
    return render(request, 'post.html', context)


def about(request):
    return render(request, 'about_page.html')


def search(request):
    """Search functionality"""
    queryset = Post.objects.all()
    query = request.GET.get('q')
    
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    
    context = {
        'object_list': queryset,
        'query': query,
    }
    return render(request, 'search_bar.html', context)


def postlist(request, slug):
    """Posts filtered by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)


def allposts(request):
    """All posts page"""
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)


def post_detail(request, pk):
    """
    Detailed post view with comments, likes, and favourites
    This is the new interactive post page
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Increment view count
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Check if user has liked or favourited
    is_liked = False
    is_favourited = False
    
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
        is_favourited = Favourite.objects.filter(user=request.user, post=post).exists()
    
    # Get all comments for this post
    comments = post.comments.all().order_by('-created_at')
    
    # Get counts
    like_count = post.like_set.count()
    favourite_count = post.favourite_set.count()
    
    context = {
        'post': post,
        'is_liked': is_liked,
        'is_favourited': is_favourited,
        'like_count': like_count,
        'favourite_count': favourite_count,
        'comments': comments,
    }
    
    return render(request, 'posts/post_detail.html', context)


@login_required
@require_POST
def toggle_like(request, pk):
    """
    Toggle like on a post
    Returns JSON response with like status and count
    """
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Unlike if already liked
        like.delete()
        liked = False
    else:
        # Like if not already liked
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': post.like_set.count()
    })


@login_required
@require_POST
def toggle_favourite(request, pk):
    """
    Toggle favourite on a post
    Returns JSON response with favourite status and count
    """
    post = get_object_or_404(Post, pk=pk)
    favourite, created = Favourite.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Remove from favourites if already favourited
        favourite.delete()
        favourited = False
    else:
        # Add to favourites if not already favourited
        favourited = True
    
    return JsonResponse({
        'favourited': favourited,
        'favourite_count': post.favourite_set.count()
    })


@login_required
def add_comment(request, pk):
    """
    Add a comment to a post
    Requires user to be logged in
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        
        if content and content.strip():
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content.strip()
            )
    
    return redirect('post_detail', pk=pk)


def about_view(request):
    """
    About page with dynamic content from admin
    Shows the active about content
    """
    about_content = About.objects.filter(is_active=True).first()
    
    context = {
        'about': about_content
    }
    return render(request, 'about_page.html', context)


# Optional: User's favourite posts view
@login_required
def my_favourites(request):
    """View user's favourite posts"""
    favourites = Favourite.objects.filter(user=request.user).select_related('post')
    posts = [fav.post for fav in favourites]
    
    context = {
        'posts': posts,
        'title': 'Mənim Favoritlərim'
    }
    return render(request, 'my_favourites.html', context)


# Optional: User's liked posts view
@login_required
def my_likes(request):
    """View user's liked posts"""
    likes = Like.objects.filter(user=request.user).select_related('post')
    posts = [like.post for like in likes]
    
    context = {
        'posts': posts,
        'title': 'Bəyəndiklərim'
    }
    return render(request, 'my_likes.html', context)

def tags_list(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags
    }
    return render(request, 'tags_list.html', context)

def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = tag.posts.all()
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})
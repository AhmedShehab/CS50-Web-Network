import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError, reset_queries
from django.http import HttpResponse, HttpResponseRedirect
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Profile


def index(request):
    all_posts = Post.objects.all().order_by('-id')
    p = Paginator(all_posts, 10)
    page_number = request.GET.get('post')
    posts = p.get_page(page_number)
    try:
        profile = Profile.objects.get(user=request.user)
        context = {
        'p': p,
        'posts': posts,
        'profile': profile if profile else None,
        'page_number': 1 if not page_number else page_number,
    }
    except:
        context = {
            'p': p,
            'posts': posts,
            'page_number': 1 if not page_number else page_number,
        }
    return render(request, "network/index.html", context)


def profile(request, profileId):
    profile = Profile.objects.get(user=profileId)
    all_posts = Post.objects.filter(author=profile.user).order_by('-id')
    p = Paginator(all_posts, 10)
    page_number = request.GET.get('post')
    posts = p.get_page(page_number)
    context = {
        'p': p,
        'posts': posts,
        'profile': profile,
        'user_profile': request.user,
        'page_number': 1 if not page_number else page_number
    }
    return render(request, 'network/profile.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request):
    try:
        post_data = json.loads(request.body)
        post_content = post_data['content']
        new_post = Post.objects.create(
            author=request.user, content=post_content)
        new_post.save()
        response = {'success': 'Post added successfully'}
    except:
        response = {"fail": "Error Saving the new Post"}
    return JsonResponse(response)


def like_post(request):
    try:
        postId = json.loads(request.body)['id']
        user = request.user
        post = Post.objects.get(id=postId)
        post.addToLiked(user)
        post.save()
        response = {'success': "Added new like"}
    except:
        response = {'fail': "Error adding new like"}
    return JsonResponse(response)


def dislike_post(request):
    try:
        postId = json.loads(request.body)['id']
        user = request.user
        post = Post.objects.get(id=postId)
        post.removeFromLiked(user)
        post.save()
        response = {'success': "Removed from likes"}
    except:
        response = {'fail': "Error removing from like"}
    return JsonResponse(response)


def profilePicture(request):
    profile = Profile.objects.get(user=request.user)
    profile.changeProfilePicture()
    return JsonResponse


def followUser(request):
    try:
        profile_id = json.loads(request.body)['id']
        profile_to_follow = Profile.objects.get(id=profile_id)
        current_user = Profile.objects.get(user=request.user)
        current_user.follow(profile_to_follow)
        profile_to_follow.followedBy(current_user)
        response = {'success': f"Successfully Followed {profile_to_follow}"}
    except:
        response = {'fail': "Error adding the user to followers"}
    return JsonResponse(response)


def unfollowUser(request):
    try:
        profile_id = json.loads(request.body)['id']
        profile_to_unfollow = Profile.objects.get(id=profile_id)
        current_user = Profile.objects.get(user=request.user)
        current_user.unfollow(profile_to_unfollow)
        profile_to_unfollow.unfollowedBy(current_user)
        response = {'success': f"Successfully unfollowed {profile_to_unfollow}"}
    except:
        response = {'fail': "Error removing the user from followers"}
    return JsonResponse(response)


@login_required(login_url='/login')
def following(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse("login"))

    all_posts = Post.objects.filter(
        author__in=profile.following.all()).order_by('-id')
    p = Paginator(all_posts, 10)
    page_number = request.GET.get('post')
    posts = p.get_page(page_number)
    context = {
        'p': p,
        'posts': posts,
        'profile': profile,
        'page_number': 1 if not page_number else page_number,
    }
    return render(request, 'network/following.html', context)


def edit_post(request):
    postData = json.loads(request.body)
    postId = postData['id']
    postContent = postData['postContent']
    postObject = Post.objects.get(id=postId)

    # For making sure that no user can change any post unless he is the author
    if postObject.author != request.user:
        return JsonResponse({
            'fail': "Error changing the post content you must be the post author"
            })
    
    postObject.content = postContent
    postObject.save()
    return JsonResponse({
        'success':"Changed post Content successfully"
    })

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("likePost", views.like_post, name="like"),
    path("dislikePost", views.dislike_post, name="dislike"),
    path("editPost",views.edit_post,name="edit"),
    path("followUser", views.followUser, name="follow"),
    path("unfollowUser", views.unfollowUser, name="unfollow"),
    path("profile/<int:profileId>",views.profile,name="profile"),
    path('changeprofilepicture',views.profilePicture,name="profilePicture"),
    path('following',views.following,name="following")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
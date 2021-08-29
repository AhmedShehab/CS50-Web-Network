from typing import Tuple
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateField
from django.db.utils import Error


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='follower')
    following = models.ManyToManyField(User, related_name="following")
    profilePicture = models.ImageField(
        null=True, blank=True, default='default.png')

    def follow(self, profile_to_follow):
        if profile_to_follow.user not in self.following.all():
            self.following.add(profile_to_follow.user)

    def followedBy(self, current_user):
        if current_user.user not in self.followers.all():
            self.followers.add(current_user.user)

    def unfollow(self, profile_to_unfollow):
        if profile_to_unfollow.user in self.following.all():
            self.following.remove(profile_to_unfollow.user)

    def unfollowedBy(self, current_user):
        if current_user.user in self.followers.all():
            self.followers.remove(current_user.user)

    def followers_count(self):
        followersCount = self.followers.all().count()
        followersCount = followersCount if followersCount else 0
        return followersCount

    def following_count(self):
        followingCount = self.following.all().count()
        followingCount = followingCount if followingCount else 0
        return followingCount

    def changeProfilePicture(self):
        self.profilePicture()

    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    dateTime = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name='whoLiked')

    def addToLiked(self, profile):
        if profile in self.likers.all():
            return Error
        self.likers.add(profile)

    def removeFromLiked(self, profile):
        if profile not in self.likers.all():
            return Error
        self.likers.remove(profile)

    def likes_count(self):
        likesCount = self.likers.all().count()
        likesCount = likesCount if likesCount else 0
        return likesCount
    
    def get_profile_picture(self):
        profile = Profile.objects.get(user=self.author)
        return profile.profilePicture
    def __str__(self) -> str:
        return f'{self.author}: {self.dateTime}'

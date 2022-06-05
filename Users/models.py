from django.db.models import *
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    name = CharField(max_length=200, blank=True, null=True)
    email = EmailField(max_length=500, blank=True, null=True)
    username = CharField(max_length=200, blank=True, null=True)
    location = CharField(max_length=200, blank=True, null=True)
    short_intro = CharField(max_length=200, blank=True, null=True)
    bio = TextField(blank=True, null=True)
    profile_image = ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = CharField(max_length=200, blank=True, null=True)
    social_twitter = CharField(max_length=200, blank=True, null=True)
    social_linkedin = CharField(max_length=200, blank=True, null=True)
    social_youtube = CharField(max_length=200, blank=True, null=True)
    social_website = CharField(max_length=200, blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    id = UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)
    class Meta:
        ordering = ['username']


class Skill(Model):
    owner = ForeignKey(Profile, on_delete=CASCADE, blank=True, null=True)
    name = CharField(max_length=200, blank=True, null=True)
    description = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    id = UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Message(Model):
    sender = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True)
    recipient = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True, related_name='messages')
    name = CharField(max_length=200, null=True, blank=True)
    email = EmailField(max_length=200, null=True, blank=True)
    subject = CharField(max_length=200, null=True, blank=True)
    body = TextField()
    is_read = BooleanField(default=False, null=True)
    created = DateTimeField(auto_now_add=True)
    id = UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']

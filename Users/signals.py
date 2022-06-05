from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings


"""
 Working with django signals:
  sender - the model that sends the signal.
  instance - object of the model
  created - boolean to tell if model was added to db or not
"""  
# @receiver(post_save, sender=Profile)  
# def profileUpdated(sender, instance, created,**kwargs):
#     print("Profile Saved")
#     print("Instance: ", instance)
#     print("Created: ", created)
    
# @receiver(post_delete,sender=Profile)
# def deleteUser(sender, instance,**kwargs):
#     print("Deleting user...")
    

# Connect the function to post_save signal
# post_save.connect(profileUpdated, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)

# Using decorators - see the functions above



"""
 Now let's create a signal that creates a user profile any time
 a user is created.
"""
@receiver(post_save, sender=User)
def createProfile(sender, instance,created,**kwargs):
    print("Created ...")
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username= user.username,
            email = user.email,
            name = user.first_name,
            
        )
        subject = "Welcome to devsearch"
        message = "We are glad you are here"
        send_mail(
          subject,
          message,
          settings.EMAIL_HOST_USER,
          [profile.email],
          fail_silently=False
        )
@receiver(post_save, sender=Profile)      
def updateUser(sender, instance, created,**kwargs):
      profile = instance
      user = profile.user
      
      if created == False:
           user.first_name = profile.name 
           user.username = profile.username
           user.email = profile.email
           user.save()
"""
  Because of the relationship, when a user is deleted, the profile is deleted too.
  Django has taken care of this. But what if the profile is deleted instead, the user is not deleted by default.
  
  To take care of this, we can use signals as shown below
"""    
@receiver(post_delete, sender=Profile)
def deleteUser(sender,instance,**kwargs):
    user = instance.user
    user.delete()
    
"""
   Now connect the signals.py to our application.
   See apps.py
"""
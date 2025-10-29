from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# This signal is triggered AFTER a User object is saved
@receiver(post_save, sender=User)
def set_new_user_permissions(sender, instance, created, **kwargs):
    # Check if this is a newly created user (not an update)
    if created:
        # 1. Set Staff Status to True
        instance.is_staff = True
        instance.save() 
        
        # 2. Add the user to the 'Reporter' Group
        try:
            reporter_group = Group.objects.get(name='Reporter')
            instance.groups.add(reporter_group)
        except Group.DoesNotExist:
            print("ERROR: 'Reporter' group does not exist. Please create it in the admin.")
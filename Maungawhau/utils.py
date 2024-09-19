from django.contrib.auth.models import User

from Maungawhau.models import Profile


def create_user_profile(username, password, first_name, last_name, email, phone, address, group):
    if User.objects.filter(username=username).exists(): #if I have duplicate
        User.objects.get(username=username).delete()  #remove old one
    if User.objects.create_user(username=username, email=email,
                                first_name=first_name,
                                last_name=last_name):
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user,
                               phone=phone,
                               address=address,
                               )
        user.groups.add(group)

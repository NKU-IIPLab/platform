from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user
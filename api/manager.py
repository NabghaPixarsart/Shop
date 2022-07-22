from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    """

    def create_user(self, email, password=None, first_name=None, last_name=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_active = True
        user.set_unusable_password()
        user.is_staff = True
        user.save()

        return user

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def create_superuser_member(self, email, password, is_superuser, is_staff, is_active, user_role, ):
        """
        Create and return a ` User` of Member superuser (Member) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        # user.is_superuser = False
        # user.is_staff = True
        user.user_role = user_role
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active

        user.save()

        return user

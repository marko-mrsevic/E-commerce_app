from django.contrib.auth.models import BaseUserManager
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    # This ensures that every authentication backend trying to authenticate the user
    # will default to a lower caps.
    def get_by_natural_key(self, username):
        return super(CustomUserManager, self).get_by_natural_key(username.lower())

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        now = timezone.now()
        email = CustomUserManager.normalize_email(email)
        user = self.model(email=email, last_login=now, **extra_fields)
        now = timezone.now()

        user.is_staff = False
        user.is_active = False
        user.is_superuser = False
        user.is_validate = False
        # Hash user password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates system administrators

        Administrator accounts are activated by default.

        Arguments:
        - `email`: provided e-mail address. Used as username.
        - `password`: provided password.
        - `**other`: remaining user metadata.
        """
        now = timezone.now()
        email = CustomUserManager.normalize_email(email)

        if not email:
            error = "E-mail address not provided!"
            raise ValueError(error)

        user = self.model(
            email=email,
            last_login=now,
            **extra_fields
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_validate = True
        # Hash user password
        user.set_password(password)
        user.save(using=self._db)

        return user

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.cache import cache


class CustomUserManager(BaseUserManager):
    def create_user(self, **args):
        if not args.get("email"):
            raise ValueError("Email vacio")
        email = self.normalize_email(args.get("email"))
        user = self.model(email=email, **args)
        user.set_password(args.get("password"))
        user.save(using=self._db)
        return user

    def create_superuser(self, **args):
        args.setdefault("is_staff", True)
        args.setdefault("is_superuser", True)

        args.setdefault("is_active", True)

        if args.get("is_staff") is not True:
            raise ValueError("El super usuario debe contar con is_staff=True")

        if args.get("is_superuser") is not True:
            raise ValueError("El super usuario debe contar con is_superuser=True.")

        return self.create_user(**args)

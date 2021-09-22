from django.db import models

class UserGroup(models.Model):

    title = models.CharField(max_length=32)


class UserInfo(models.Model):

    user_type_choices = (
        (1, '普通用户'),
        (2, 'vip'),
    )

    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey("UserGroup", null=True, blank=True, on_delete=models.SET_NULL)
    roles = models.ManyToManyField("Role")


class UserToken(models.Model):

    user = models.OneToOneField(to='UserInfo',null=True, blank=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length = 64)


class Role(models.Model):

    title = models.CharField(max_length=32)
from django.contrib.auth.models import User
from mcdashbeckend.mcdashadmin.models import Employee
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
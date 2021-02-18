from enum import unique

from django.db.models import fields
from mcdashadmin.models import Employee, Shift, Staff, Shift_Detail, Store
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterationSerializer(serializers.ModelSerializer):
    staff_position = serializers.CharField(max_length=100)
    password2 = serializers.CharField(style={"input-type": 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'staff_position']

    def save(self):
        pass1 = self.validated_data['password']
        pass2 = self.validated_data['password2']
        staff = Staff.objects.get(position= self.validated_data['staff_position'])

        if pass1 == pass2:
            if staff is not None:
                user = User(
                    username = self.validated_data['username'],
                    first_name = self.validated_data['first_name'],
                    last_name = self.validated_data['last_name'],
                    email = self.validated_data['email']
                )
                user.set_password(pass1)
                user.save()
                Employee.objects.create(user=user, staff=staff)
                return user
            else:
                raise serializers.ValidationError({'staff_position': 'position is not found'})
        else:
            raise serializers.ValidationError({'password': 'password does not match'})

class shift_detail_serializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()
    class Meta:
        model = Shift_Detail
        fields = ['start_at', 'end_at', 'station', 'store_name']

    def get_store_name(self, obj):
        store = Store.objects.get(pk=obj.store.id)
        return store.name
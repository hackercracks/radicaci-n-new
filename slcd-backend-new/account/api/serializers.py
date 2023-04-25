from rest_framework import serializers
from account.models import User, UserProfile
from filed.models import Agent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'is_organisor', 'is_agent', 'is_support']


class SignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2', 'is_organisor', 'is_agent', 'is_support']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_organisor= self.validated_data['is_organisor']
        user.is_agent= self.validated_data['is_agent']
        user.is_support= self.validated_data['is_support']
        user.save()
        if user.is_organisor == True:
            UserProfile.objects.create(user=user)
        if user.is_support == True:
            UserProfile.objects.create(user=user)
        if user.is_agent == True:
            Agent.objects.create(user=user)
        return user


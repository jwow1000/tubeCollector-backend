from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tube, Playlist

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class TubeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tube
    fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
  tubes = TubeSerializer(many=True, read_only=True)
  users = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Playlist
    fields = '__all__'

  



from rest_framework import generics, status, permissions 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Tube, Playlist
from .serializers import TubeSerializer, PlaylistSerializer, UserSerializer

# # # # # # # # #   User verification views:   # # # # # # # # # # # # 
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]
  def post(self, request):
    print("check on request", request.data.get)
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

# define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to tubeCollector!'}
    return Response(content)

# views for playlists
class PlaylistList(generics.ListCreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    # This ensures we only return playlists belonging to the logged-in user
    user = self.request.user
    return Playlist.objects.filter(user=user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = PlaylistSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Playlist.objects.filter(user=user)
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # toys_not_associated = Toy.objects.exclude(id__in=instance.toys.all())
    tubes_serializer = TubeSerializer(many=True)

    return Response({
        'playlist': serializer.data,
        'tubes': tubes_serializer.data
    })
  
  def perform_update(self, serializer):
    plist = self.get_object()
    if plist.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this cat."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this cat."})
    instance.delete()


# basic routes for the tubes
class TubeList(generics.ListCreateAPIView):
  queryset = Tube.objects.all
  serializer_class = TubeSerializer

class TubeDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tube.objects.all()
  serializer_class = TubeSerializer
  lookup_field = 'id'

# class TubeChangePosition(APIView):
#   def patch(self, request, id, *args, **kwargs):
#     tube = Tube.objects.get(id=id)
#     tube.posX = kwargs['posX']
#     tube.posY = kwargs['posY']
#     return Response({'message': f'Tube: {tube.title} position is now: {tube.posX}, {tube.posY}'})

class AddTubeToPlaylist(APIView):
  def post(self, request, plist_id, tube_id):
    plist = Playlist.objects.get( id=plist_id )
    tube = Tube.objects.get( id=tube_id )
    plist.tubes.add(tube)
    return Response( {'message': f'Tube: {tube.title}, added to Playlist: {plist.title}'})

class RemoveTubeFromPlaylist(APIView):
  def post(self, request, plist_id, tube_id):
    plist = Playlist.objects.get( id=plist_id )
    tube = Tube.objects.get( id=tube_id )
    plist.tubes.remove(tube)
    return Response( {'message': f'Tube: {tube.title}, removed from Playlist: {plist.title}'})
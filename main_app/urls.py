from django.urls import path
from .views import Home, TubeList, TubeDetail, PlaylistDetail, PlaylistList, AddTubeToPlaylist, RemoveTubeFromPlaylist, CreateUserView, LoginView, VerifyUserView, PlaylistCreate

urlpatterns = [
  # home route
  path('', Home.as_view(), name='home'),
  
  # tube routes
  path('tubes/', TubeList.as_view(), name="tube-list"),
  path('tubes/<int:id>/', TubeDetail.as_view(), name="tube-detail"),
  # path('tubes/<int:id>/change_pos', TubeChangePosition.as_view(), name="tube-change-pos"),


  # playlist routes
  path('playlists/', PlaylistList.as_view(), name="playlist-list"),
  path('playlists/<int:id>/', PlaylistDetail.as_view(), name="playlist-detail"),
  path('playlists/create/', PlaylistCreate.as_view(), name='playlist-create'),


  path('playlists/<int:plist_id>/add_tube/<int:tube_id>/', AddTubeToPlaylist.as_view(), name='add-tube-to-playlist'),
  path('playlists/<int:plist_id>/remove_tube/<int:tube_id>/', RemoveTubeFromPlaylist.as_view(), name='remove-tube-from-playlist'),

  # REST/JWT routes
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

]

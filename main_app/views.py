from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

# define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to tubeCollector!'}
    return Response(content)

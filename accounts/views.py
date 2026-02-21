from rest_framework import generics,permissions
from .models import User
from .serializers import RegisterSerializer,UserSerializer
from .permissions import IsAdmin

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [IsAdmin]

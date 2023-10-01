from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from djangoProject.permissions import IsOwnerOrReadOnly
from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserUpdateDataSerializer, RegisterSerializer, \
    UserLogoutSerializer, UserDataSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UsersModelView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = UserDataSerializer
    http_method_names = ['get', 'patch', 'retrieve', ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'author', 'object_id', 'content_type']
    ordering_fields = ['id', 'email', 'last_login', 'date_joined']

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateDataSerializer
        return self.serializer_class


class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    queryset = User.objects.all()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=UserLogoutSerializer)
    def post(self, request):
        refresh = request.data.get('refresh', None)
        if refresh is not None:
            try:
                token = RefreshToken(request.data.get('refresh', None))
                token.blacklist()
                return Response("Success")
            except TokenError as e:
                return Response(str(e), status=200)
        else:
            return Response('Token is required', status=400)

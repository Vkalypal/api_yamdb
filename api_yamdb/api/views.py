from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import SignUpSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework import serializers
from rest_framework import viewsets
from .permissions import AdminOnly
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
from .serializers import GetTokenSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username',)


class SignUpViewSet(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
    'Тема письма',
    confirmation_code,
    'practicum29team@mail.ru',
    [serializer.validated_data['email']],
    fail_silently=False, 
) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    user = get_object_or_404(User, username)
    confirmation_code = serializer.validated_data.get("confirmation_code")
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return token
    else:
        raise serializers.ValidationError("Код не верный")

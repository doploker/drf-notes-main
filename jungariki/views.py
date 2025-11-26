from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from jungariki.serializer import UserSerializer, AuthUserSerializer


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginUser(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = AuthUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            token, create = Token.objects.get_or_create(user=user)

            return Response({
                'id': user.id,
                'username': user.username,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        error_message = serializer.errors
        return Response({
            'errors': error_message,
            'success': False,
        }, status = status.HTTP_400_BAD_REQUEST)

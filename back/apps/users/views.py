from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserAIConfigSerializer
from .models import UserAIConfig


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserAIConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            config = request.user.ai_config
            serializer = UserAIConfigSerializer(config)
            data = serializer.data
            data['api_key'] = config.api_key[:8] + '****' if len(config.api_key) > 8 else '****'
            return Response(data)
        except UserAIConfig.DoesNotExist:
            return Response({'provider': 'openai', 'api_key': '', 'api_url': '', 'model_name': '', 'is_active': False})

    def post(self, request):
        try:
            config = request.user.ai_config
            serializer = UserAIConfigSerializer(config, data=request.data, partial=True)
        except UserAIConfig.DoesNotExist:
            serializer = UserAIConfigSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            config = request.user.ai_config
            config.delete()
            return Response({'message': '配置已删除'})
        except UserAIConfig.DoesNotExist:
            return Response({'error': '配置不存在'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from typing import Dict, Any
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        data['user'] = {
            'username': self.user.username,
            'message': True
        }
        data.pop('refresh')
        data.pop('access')
        # data["refresh"] = str(refresh)
        # data["access"] = str(refresh.access_token)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutAPiView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            print(token.token)
            token.blacklist()
            data = {
                'success': True,
                'message': 'Token saved Blacklisted'
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


IsAuthenticated
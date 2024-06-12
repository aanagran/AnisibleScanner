from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from users.serailizers import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.utils import portal_jwt_token_update



class LoginView(APIView):
    # throttle_classes = [CustomScopedRateThrottle]
    throttle_scope = None
    def post(self, request):
        try:
            data = request.data
            userloginserializer= UserLoginSerializer(data=request.data)
            if userloginserializer.is_valid():
                validated_data=userloginserializer.validated_data
                username = validated_data.get('username',None)
                password = validated_data.get('password',None)
                user = authenticate(username=username, password=password)
                if user:
                    token_data = RefreshToken.for_user(user)
                    token_data = portal_jwt_token_update(user,token_data)
                else:
                    cont = {'message': 'Invalid Username or Password'}
                    return Response(cont,status=status.HTTP_401_UNAUTHORIZED)
                access_token=token_data.access_token
                refresh_token = token_data
                data={
                    'access_token' : str(access_token),
                    'refresh_token': str(refresh_token)
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(userloginserializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("[ERROR ] : Exception occured in login -> ",error)
            # logging.info("[ERROR ] : Exception occured in login -> ",error)
            return Response({"message":"INTERNAL Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

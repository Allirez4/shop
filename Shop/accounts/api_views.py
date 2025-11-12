from rest_framework.response import Response
from rest_framework.views import APIView
from . serializers import UserLoginserializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
class login_api(APIView):
    """
    API view for user authentication and login.
    This view handles user login requests using either email or phone number ONLY one
    as the username field along with a password. Upon successful authentication,
    it generates JWT access and refresh tokens for the user session.
    Attributes:
        serializer_class: UserLoginserializer - Serializer for validating login data
        authentication_classes: list - Empty list to allow unauthenticated access
    Methods:
        post(request): Processes login requests and returns JWT tokens on success
    Request Data:
        - email (str, optional): User's email address
        - phone_number (str, optional): User's phone number  
        - password (str, required): User's password
    Returns:
        Response: JSON response containing:
            - On success (200): message, access token, refresh token
            - On failure (401): error message for invalid credentials
    Raises:
        ValidationError: If serializer validation fails
    """
    serializer_class=UserLoginserializer
    authentication_classes=[]
    
    def post(self,request):
        data=request.data
        serializer=UserLoginserializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data=serializer.validated_data
            print(data)
            print(data.get('email'),data.get('phone_number'))
            if data.get('email'):
                user=authenticate(request,username=data['email'],password=data['password'])
                token=RefreshToken.for_user(user)
                access=str(token.access_token)
                refresh=str(token)
                if user:
                    return Response({'message':'Login successful','access':access,'refresh':refresh},status=200)
                else: 
                    return Response({'message':'wrong email  or password credentials'},status=401)
            elif data.get('phone_number'):
                user=authenticate(request,phone_number=data['phone_number'],password=data['password'])
                if user: 
                    token=RefreshToken.for_user(user)
                    access=str(token.access_token)
                    refresh=str(token)
                    return Response({'message':'Login successful','access':access,'refresh':refresh},status=200)    
                else: return Response({'message':'wrong password or phone number credentials'},status=401)
        else:
            return Response({'message':'Invalid credentials'},status=401)
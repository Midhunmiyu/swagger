from rest_framework.views import APIView,status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from polls.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



User = get_user_model()

class RegisterView(APIView):
    def post(self,request):
        try:
            username = request.POST.get('uname')
            email = request.POST.get('email')
            password = request.POST.get('pass')

            user = User.objects.create_user(username=username,email=email,password=password)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            return Response({"status":True,"message":"User Register Successfully....!!!","refresh_token":refresh_token,"access_token":access_token},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Log in with username and password to get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Your username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                }
            ),
            401: "Invalid credentials",
        },
    )
    def post(self,request):
        try:
            print(request.data)
            uname = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request,username=uname,password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                return Response({"status":True,"message":"User Register Successfully....!!!","refresh_token":refresh_token,"access_token":access_token},status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False,"message":"Invalid Credentials..!!!"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users. Authentication is required.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Operation status'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Operation message'),
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)  # You can specify user fields here.
                    ),
                }
            ),
            401: "Unauthorized - Authentication credentials not provided or invalid.",
        },
    )

    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response({"status":True,"message":"Successfully Retrieved Users","data":serializer.data},status=status.HTTP_200_OK)
        
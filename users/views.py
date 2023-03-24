from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics,status
from rest_framework.response import Response
from users.emails import send_otp_via_email
from django.contrib.auth import authenticate
from users.serializers import *
from utils.weather import getweather

# Create your views here.
class RegiserUser(generics.GenericAPIView) :
    serializer_class = RegisterSerializer
    def post(self, reque):
        try:
            data = reque.data
            serializers = RegisterSerializer(data = data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                send_otp_via_email(serializers.data['email'])
                return Response({
                    "status" : 200,
                    'massege' : 'registration successfully check email',
                    'data' : serializers.data,
                    })
            else:
                return Response({
                        "status" : 400,
                        'massege' : 'somthings went wrong',
                        'data' : serializers.errors,
                        })
        except Exception as e:
            print(e)
            return Response({
                    "status" : 400,
                    'massege' : 'somthings went wrong',
                    'data' : "NO Data",
                    })
        
class UserEmaiVerifyOTP(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer
    def post(self , requs):
        try: 
           data = requs.data
           serializers =  VerifyAccountSerializer(data= data)
           if serializers.is_valid(raise_exception=True):
               email = serializers.data['email']
               otp = serializers.data['otp']

               user = User.objects.get(email = email)
               if user:
                   if user.otp == otp:
                       user.is_verified = True
                       user.save()
                       return Response({
                        "status" : 200,
                        'massege' : 'Account Verified',
                        'data' : {},
                        })
                   else :
                       return Response({
                            "status" : 400,
                            'massege' : 'somthings went wrong',
                            'data' : "wrong OTP",
                        })
               else :
                   return Response({
                        "status" : 400,
                        'massege' : 'somthings went wrong',
                        'data' : "invalid email",
                    })
           return Response({
                    "status" : 400,
                    'massege' : 'somthings went wrong',
                    'data' : serializers.errors,
                    })
        except Exception as e:
            print(e)
            return Response({
                    "status" : 400,
                    'massege' : 'somthings went wrong',
                    'data' : serializers.errors,
                    })


class LoginView(generics.GenericAPIView):
    """
    User Login
    """
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email", "")
        password = data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user:
            serializer_class = self.get_serializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                if not user.is_verified:
                    message = "account_not_verified"
                    return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    user_data = {"user_id": user.id, "email":user.email, "tokens":user.tokens}
                    message = "login_success"
                    return Response({'message':message, 'data':user_data}, status=status.HTTP_200_OK)
        message = "login_invalid_credentials"
        return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
    

class GetWeather(generics.GenericAPIView):
    serializer_class = GetWeatherSerializer
    permission_classes = [IsAuthenticated,AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            city = request.data['city']
            if city:
                data = getweather(city=city)
                return Response({'message': "success" , "data":data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Failed" , "data":{"city": ["This field may not be blank."],}}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': "Failed" , "data":"No data"}, status=status.HTTP_400_BAD_REQUEST)
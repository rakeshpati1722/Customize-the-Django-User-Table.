from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import CustomModel
from app.serializers import SignupSerializer,LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from app.models import OTP
from rest_framework.permissions import IsAuthenticated,AllowAny

User = get_user_model()
# Create your views here.

class SignupView(APIView):
    serializer_class = SignupSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            fname = serializer.data['First_name']
            lname = serializer.data['Last_name']
            gender = serializer.data['gender']
            email = serializer.data['email']
            phone_number = serializer.data['phone_number']
            
            user = User(first_name=fname,last_name=lname,gender=gender,email=email,phone_number=phone_number)
            user.save()
            content = {
                  'first_name':fname,
                  'last_name':lname,
                  'gender':gender,
                  'email':email,
                  'phone_number':phone_number  
            }    
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)    

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            otp = serializer.data['otp']
            try:
                user = get_user_model().objects.get(email=username)
            except get_user_model().DoesNotExist:
                print("user not found") 
                user = None   
            try:
                ot = OTP.objects.get(otp=otp) 
                print(ot)   
            except OTP.DoesNotExist:
                print("otp does not exist")
                ot = None    

            if user != None and ot != None:
                content = {"message":"login successfull"}
                return Response(content,status=status.HTTP_201_CREATED)
            else:
                content = {"message":"failed to login"}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)        

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        print(user)
        ot = OTP.objects.get(user=user)
        o = ot.delete()
        content = {"message":"user logged out"}
        return Response(content,status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .serializers import (
    UserRegisterSerializer, 
    UserDetailsSerializer, 
    ChangePasswordSerializer,
    LogoutSerializer  # დარწმუნდი, რომ ეს სერიალაიზერი გაქვს serializers.py-ში, ან ქვემოთ მოცემულია
)

User = get_user_model()

# 1. რეგისტრაცია (Auth)
@extend_schema(
    tags=['Auth'],
    request=UserRegisterSerializer
)
class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "იუზერი წარმატებით დარეგისტრირდა!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. ლოგინი შესაბამისი აღწერით და auth ჯგუფით
@extend_schema(
    tags=['auth'],
    description="Log in and obtain a JWT access/refresh token pair."
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


# 3. პროფილის ნახვა და განახლება (Account)
@extend_schema(tags=['Account'])
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# 4. ანგარიშის წაშლა (Account)
@extend_schema(tags=['Account'])
class UserDeleteAPIView(DestroyAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# 5. პაროლის შეცვლა (Account)
@extend_schema(
    tags=['Account'],
    request=ChangePasswordSerializer
)
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["ძველი პაროლი არასწორია."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "პაროლი წარმატებით შეიცვალა!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 6. ლოგაუთი (Auth)
@extend_schema(
    tags=['Auth'],
    request=LogoutSerializer
)
class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "წარმატებით გამოხვედით სისტემიდან."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "არასწორი თოქენი ან სესია."}, status=status.HTTP_400_BAD_REQUEST)


# 7. თოქენის განახლება (api ჯგუფი)
@extend_schema(tags=['api'])
class CustomTokenRefreshView(TokenRefreshView):
    pass
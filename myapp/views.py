from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .Serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializers import TransactionSerializer
from .Serializers import CategorySerializer,ChangePasswordSerializer

from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Transaction
from .models import Category

class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ProtectedExampleView(APIView):
    permission_classes = [IsAuthenticated]
    print('hel')
    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Transaction.objects.filter(UserID=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        print('data is coming')
        if serializer.is_valid():
            print('data is com')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        print(f"Received pk: {request.data.get('id')}")
        instance = get_object_or_404(Transaction, pk=request.data.get('id'))
        print(f"Found instance: {instance}")

        serializer = TransactionSerializer(instance=instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        print(f"Received delete request for pk: {pk}")
        print(f"User: {request.user}")
        transaction = get_object_or_404(Transaction, pk=pk, UserID=request.user)
        print(f"Found transaction: {transaction}")
        transaction.delete()
        return Response({"detail": "Transaction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    print('hel')
    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Category.objects.filter(UserID=user)
        serializer = CategorySerializer(transactions, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        print('data is coming')
        if serializer.is_valid():
            print('data is com')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        print(f"Received pk: {request.data.get('id')}")
        instance = get_object_or_404(Category, pk=request.data.get('id'))
        print(f"Found instance: {instance}")

        serializer = CategorySerializer(instance=instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        print(f"Received delete request for pk: {pk}")
        print(f"User: {request.user}")
        transaction = get_object_or_404(Category, pk=pk, UserID=request.user)
        print(f"Found transaction: {transaction}")
        transaction.delete()
        return Response({"detail": "Transaction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
      
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    print('hel')
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email
        }, status=200)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Assuming token authentication is used
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            # Check old password
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
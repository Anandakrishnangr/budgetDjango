from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Transaction
from .models import Category



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add password as write-only field

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Include password here for validation

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('UserID',)


    def create(self, validated_data):
        validated_data['UserID'] = self.context['request'].user

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.Amount = validated_data.get('Amount', instance.Amount)
        instance.CategoryID = validated_data.get('CategoryID', instance.CategoryID)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.TransactionDate = validated_data.get('TransactionDate', instance.TransactionDate)
        instance.TransactionType = validated_data.get('TransactionType', instance.TransactionType)
        instance.save()
        return instance
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('UserID',)


    def create(self, validated_data):
        validated_data['UserID'] = self.context['request'].user

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.Name = validated_data.get('Name', instance.Name)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.TransactionDate = validated_data.get('TransactionDate', instance.TransactionDate)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Add any additional password validations here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
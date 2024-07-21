from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Transaction
from .models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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
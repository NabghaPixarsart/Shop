from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CoreUser, Shop
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CoreUser.objects.create_user(email=validated_data['email'], password=validated_data['password'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'])
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        tokens = CoreUser.tokens(user)

        return {
            'email': user.email,
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ('first_name', 'last_name', 'phone')


class ShopSerializer(ModelSerializer):
    try:
        class Meta:
            model = Shop
            fields = '__all__'

        def create(self, validated_data):
            if Shop.objects.filter(seller_id=validated_data['seller_id']).exists():
                raise serializers.ValidationError("User Already exists.")
            new_shop = Shop.objects.create(
                title=validated_data['title'],
                description=validated_data['description'],
                location=validated_data['location'],
                seller_id=validated_data['seller_id']
            )
            return new_shop
    except Exception as e:
        print(f'[ShopSerializer] serializer throws exception {e}')


class ShopUserSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['seller_id'] = f"{instance.seller_id.id}"
        return response

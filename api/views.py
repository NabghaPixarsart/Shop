from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CoreUser, Shop
from .serializers import RegisterSerializer, UserSerializer, UserLoginSerializer, ShopSerializer, ShopUserSerializer
from rest_framework import status


class RegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }, status.HTTP_200_OK
            )
        else:
            print(f'serializer throws exception {serializer.errors}')
            response = {
                'success': False,
                'message': f'Serializer throws exception {serializer.errors}'
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # token = json.load(json_response)
                # print("token:", type(token))
                # print("access_token:", token['access_token'])
                # print("refresh_token:", token['refresh_token'])
                # serializer.save()
                # print(serializer.validated_data)
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUser(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            phone = request.data.get('phone', None)
            permissions = request.data.get('permissions', None)
            core_id = id if id else request.user.id

            target_user = CoreUser.objects.filter(id=core_id)
            if target_user:
                if first_name:
                    target_user.update(first_name=first_name)
                if last_name:
                    target_user.update(last_name=last_name)
                if phone:
                    target_user.update(phone=phone)
                if permissions:
                    target_user.update(permissions=permissions)

                updated_user_details = CoreUser.objects.filter(id=core_id).all() \
                    .values('first_name', 'last_name', 'email', 'phone', )

                updated_user = updated_user_details[0] if updated_user_details else None
                response = {
                    'success': True,
                    'message': 'User details updated successfully',
                    'first_name': updated_user['first_name'],
                    'last_name': updated_user['last_name'],
                    'email': updated_user['email'],
                    'phone': updated_user['phone'],
                    # 'updated_details': updated_user
                }

                return Response(response, status.HTTP_200_OK)

            else:
                response = {
                    'success': True,
                    'message': 'target user not found'
                }

                return Response(response, status.HTTP_200_OK)

        except Exception as e:

            response = {
                'success': False,
                'message': f'bad request {e}'
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:

            # id = request.GET.get('id', None)
            id = request.data.get('id', None)
            if id:
                result = CoreUser.objects.filter(id=id, is_expired=False) \
                    .update(is_expired=True, is_active=False)
                print(result)
                if result == 1:
                    response = {
                        'success': True,
                        'message': 'User deleted successfully'
                    }
                    return Response(response, status.HTTP_200_OK)
                else:
                    response = {
                        'success': True,
                        'message': 'User not found'
                    }
                    return Response(response, status.HTTP_200_OK)
            else:
                response = {
                    'success': False,
                    'message': 'User id is not provided'
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': f'bad request {e}'
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }, status.HTTP_200_OK
            )
        else:
            print(f'serializer throws exception {serializer.errors}')
            response = {
                'success': False,
                'message': f'Serializer throws exception {serializer.errors}'
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)


class ShopView(APIView):
    def post(self, request):
        try:
            request.data._mutable = True
            request.data['seller_id'] = request.user.id
            serializer = ShopSerializer(data=request.data)
            request.data._mutable = False
            if serializer.is_valid():
                serializer.save()
                response = {
                    'success': True,
                    'message': 'Successfully created',
                    'shop_id': serializer.data['id']
                }

                return Response(response, status=status.HTTP_200_OK)
            else:
                print(type(serializer.errors))
                response = {
                    'success': False,
                    'message': serializer.errors
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': f'bad request {e}'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ShopApi(APIView):

    def put(self, request):
        try:
            # if Shop.objects.filter(seller_id=request.user.id).exists():
            #     raise
            shop_object = Shop.objects.filter(seller_id=request.user.id)
            title = request.data.get('title', None)
            location = request.data.get('location', None)
            description = request.data.get('description', None)
            if shop_object is not None:
                if title is not None:
                    shop_object.update(title=title)

                if description is not None:
                    shop_object.update(description=description)

                if location is not None:
                    shop_object.update(location=location)
                response = {
                    'success': True,
                    'message': 'Susseccfully updated'
                }
                return Response(response, status.HTTP_200_OK)
            # serializer = ShopUserSerializer(shop_object)
            # if serializer.is_valid():
            #     # serializer.save()
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class UserShopView(APIView):
    """offersView class
        This view performs GET,PUT and DELETE operations for FAQ
        Parameters
        ----------
        APIView : rest_framework.views
        """

    def get(self, request, ):
        try:
            shop_object = Shop.objects.filter(seller_id=request.user.id).all().values()
            shop_data = shop_object[0] if shop_object else None
            if shop_data:
                response = {
                    'success': True,
                    'message': 'Shop details',
                    'title': shop_data['title'],
                    'description': shop_data['description'],
                    'location': shop_data['location']
                }
                return Response(response, status.HTTP_200_OK)
            # serializer = ShopUserSerializer(shop_object)
            # return Response(serializer.data, status=status.HTTP_200_OK)

        except Shop.DoesNotExist:
            return Response({"message": f"user object does not exist against {id}"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




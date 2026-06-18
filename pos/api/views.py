from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
# import model
from pos_app.models import User, TableResto, StatusModel, Category, MenuResto
# import serializer
from api.serializers import RegisterUserSerializer, LoginSerializer,TableRestoSerializer, MenuRestoSerializer,CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

#import uutk generic clan dan filters
from rest_framework import generics, filters

# import token
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate


#import permission
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.permissions import IsAuthenticated, AllowAny



class RegisterUserAPIView(APIView):
  serializer_class = RegisterUserSerializer
  permission_classes = [AllowAny]
  authentication_classes = []
  def post(self, request, format = None):
      serializer = self.serializer_class(
          data=request.data,
          context={'request': request}
      )
      if serializer.is_valid():
        serializer.save()
        response_data = {
          'status' : status.HTTP_201_CREATED,
          'message' : 'selamat anda sudah terdaftar',
          'data' : serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
      return Response({
        'status' : status.HTTP_400_BAD_REQUEST,
        'data' : serializer.errors
      }, status=status.HTTP_400_BAD_REQUEST)

# Login User View
class LoginView(APIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]
  authentication_classes = []

  def post(self, request):
      serializer = LoginSerializer(data = request.data)
      serializer.is_valid(raise_exception= True)
      user = serializer.validated_data['user']
      django_login(request, user)

      token, created = Token.objects.get_or_create(user = user)

      return JsonResponse({
        'status' : 200,
        'message' : 'Selamat anda berhasil masuk...',
        'data' : {
          'token' : token.key,
          'id' : user.id,
          'first_name' : user.first_name,
          'last_name' : user.last_name,
          'email' : user.email,
          'is_active' : user.is_active,
          'is_watress' : user.userprofile.is_waitress,
        }
      })

# logout controller

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        django_logout(request)

        return Response({
            "status": 200,
            "message": "Logout berhasil. Token dan session telah dihapus."
        }, status=status.HTTP_200_OK)



class TableRestoListApiView(APIView):
  permission_classes = [AllowAny]
  def get(self, request, *args, **kwargs):
    table_resto = TableResto.objects.all()
    serializer = TableRestoSerializer(table_resto , many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
      data = {
        'code': request.data.get('code'),
        'name': request.data.get('name'),
        'capacity': request.data.get('capacity'),
      }

      serializer = TableRestoSerializer(data = data)

      if serializer.is_valid():
        serializer.save()
        response = {
          'status' : status.HTTP_200_OK,
          'message' : 'Data created successfully...',
          'data' : serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableRestoDetailApiView(APIView):
  permission_classes = [AllowAny]
  def get_object(self, id):
      try:
        return TableResto.objects.get(id = id)
      except TableResto.DoesNotExist:
        return None

  def get(self, request, id, *args, **kwargs):
      table_resto_instance = self.get_object(id)
      if not table_resto_instance:
        return Response(
          {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'data does not exist...',
            'data' : {}
          }, status.HTTP_400_BAD_REQUEST
        )

      serializer = TableRestoSerializer(table_resto_instance)
      response = {
        'status' : status.HTTP_200_OK,
        'message' : 'Data retrieve Succefull..',
        'data' : serializer.data
      }
      return Response(response, status= status.HTTP_200_OK)


  def put(self, request, id, *args, **kwargs):
      table_resto_instance = self.get_object(id)
      if not table_resto_instance:
        return Response(
          {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message': 'Data does not exist',
            'data' : {}
          }, status = status.HTTP_400_BAD_REQUEST
        )

      data = {
          'code' : request.data.get('code'),
          'name' : request.data.get('name'),
          'capacity' : request.data.get('capacity'),
          'table_status' : request.data.get('table_status'),
          'status' : request.data.get('status')
        }
      serializer = TableRestoSerializer(instance = table_resto_instance, data = request.data, partial = True)

      if serializer.is_valid():
          serializer.save()
          response = {
            'status' : status.HTTP_200_OK,
            'mesagge': 'data update succefully',
            'data' : serializer.data
          }
          return Response(response, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, *args, **kwargs):
      table_resto_instance = self.get_object(id)
      if not table_resto_instance:
        return Response(
          {
            'status' : status.HTTP_400_BAD_REQUEST,
            'mesagge' : 'Data does not exist',
            'data' : {}
          }, status=status.HTTP_400_BAD_REQUEST
        )

      table_resto_instance.delete()
      response = {
        'status' : status.HTTP_200_OK,
        'message': 'Data deleted Successfully...'
      }
      return Response(response, status=status.HTTP_200_OK)



# =====================
# pakek Generic Class
# ====================

# list data
# class TableRestoList(generics.ListAPIView):
#   queryset = TableResto.objects.all()
#   serializer_class = TableRestoSerializer
#   permission_classes = [AllowAny]

# # Create data
# class TableRestoCreate(generics.CreateAPIView):
#   queryset = TableResto.objects.all()
#   serializer_class = TableRestoSerializer

# ==================================================



# Menu resto View
class MenuRestoView(generics.ListAPIView):
  queryset = MenuResto.objects.all()
  serializer_class = MenuRestoSerializer
  permission_classes = [AllowAny]
# Menu resto View

class CategoryView(generics.ListAPIView):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer  
   permission_classes = [AllowAny] 


# Pagination
from .pagination import CustomPagination

class MenuRestoFirterApi(generics.ListAPIView):
  queryset = MenuResto.objects.all()
  serializer_class = MenuRestoSerializer
  pagination_class = CustomPagination
  permission_classes = [AllowAny]
  # permission_classes = []
  filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
  filterset_fields = ['category__name']
  ordering_fields = ['created_on']

# controller menu resti with permision
class MenuRestoPermissionView(APIView):
  authentication_classes = [
                            TokenAuthentication,
                            SessionAuthentication,
                            BasicAuthentication
                          ]
  permission_classes = [IsAuthenticated]


  def get(self, request, *args, **kwargs):
      menu_restos = MenuResto.objects.select_related('status').filter(status = StatusModel.objects.first())
      serializer = MenuRestoSerializer(menu_restos, many = True)
      response = {
        'status' : status.HTTP_200_OK,
        'message' : 'Pembacaan seluruh data berhasil...',
        'user' : str(request.user),
        'auth' : str(request.auth),
        'data' : serializer.data
      }
      return Response(response, status=status.HTTP_200_OK)




def get_csrf(request):
    return JsonResponse({
        'message': 'CSRF cookie set'
    })

















# class LoginView(APIView):

#     permission_classes = []

#     def post(self, request):

#         user = authenticate(
#             username=request.data.get("username"),
#             password=request.data.get("password")
#         )

#         if not user:
#             return Response({"message": "Login gagal"}, status=400)

#         token, created = Token.objects.get_or_create(user=user)

#         return JsonResponse({
#             "status": 200,
#             "message": "Login sukses",
#             "data": {
#                 "token": token.key,
#                 "user_id": user.id,
#                 "username": user.username
#             }
#         })


# class LogoutView(APIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         # hapus token user
#         request.user.auth_token.delete()

#         return Response({
#             "status": 200,
#             "message": "Logout berhasil (token dihapus)"
#         })
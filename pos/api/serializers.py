from rest_framework import serializers
from pos_app.models import (
  User, UserProfile, TableResto, MenuResto, Category
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


# Register user
class RegisterUserSerializer(serializers.ModelSerializer):
  is_waitress = serializers.SerializerMethodField(read_only=True)
  email = serializers.EmailField(
    required = True,
    validators = [UniqueValidator(queryset= User.objects.all())]
  )
  password1 = serializers.CharField(
    write_only = True,
    required = True,
    validators = [validate_password]
  )

  password2 = serializers.CharField(
    write_only =  True,
    required = True
  )

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_waitress','first_name', 'last_name']
    extra_kwargs = {
      'first_name' : { 'required' : True },
      'last_name' : { 'required' : True }
    }
    
  def get_is_waitress(self, obj):
    return obj.userprofile.is_waitress

  def validate(self, attrs):
    if attrs['password1'] != attrs['password2']:
      raise serializers.ValidationError({
        'password' : 'Kata sandi dan Ulang kata sandi tidak sama'
      })
    return attrs

  def create(self, validated_data):
    request = self.context.get('request')
    is_waitress = str(request.data.get('is_waitress', '0')) == '1'
    user = User.objects.create(
      username = validated_data['username'],
      email = validated_data['email'],
      is_active = validated_data['is_active'],
      # is_waitress = validated_data['is_waitress'],
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name']
    )
    user.set_password(validated_data['password1'])
    user.save()
    UserProfile.objects.create(
        user=user,
        is_waitress=is_waitress
    )
    return user
  
# User login
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()
  
  def validate(self, data):
    username = data.get('username', '')
    password = data.get('password', '')

    if username and password:
      user = authenticate(username = username, password = password)
      if user:
        if user.is_active and user.userprofile.is_waitress:
          data['user'] = user
        else:
          msg = 'Status Pengguna Tidak Aktif...'
          raise ValidationError({
            'message' : msg
          })
      else:
        msg = 'Anda Tidak memiliki akses masuk'
        raise ValidationError({
          'message': msg
        })
    else:
      msg = 'Mohon mengisi kolom nama pengguna dan kata sandi'
      raise ValidationError({
        'message' : msg
      })
    
    return data

class TableRestoSerializer(serializers.ModelSerializer):
  class Meta:
    model = TableResto
    # fields = '__all__'
    fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status')

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class MenuRestoSerializer(serializers.ModelSerializer):
  category = serializers.CharField(
    source = 'category.name',
    read_only = True
  )
  class Meta:
    model = MenuResto
    fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 'category', 'menu_status', 'status')
from rest_framework import serializers
from pos_app.models import (
  User, UserProfile, TableResto, MenuResto, Category,OrderDetail,Order,StatusModel
)
from django.contrib.auth.models import User
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
    category = serializers.CharField(source = 'category.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)
    
    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 
            'category', 'menu_status', 'status')
        
class MenuRestoFilterSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)

    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 
            'category', 'menu_status', 'status')

class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id', 'order', 'menu_resto', 'quantity', 'subtotal')

class OrderCreateSerializer(serializers.ModelSerializer):
    order_order_detail = OrderDetailCreateSerializer(many = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_order_detail', 'order_status', 
            'total_order', 'tax_order', 'total_payment', 'user_create')
    
    def create(self, validated_data):
        order_items = validated_data.pop('order_order_detail')
        order = Order.objects.create(**validated_data)

        # Save OrderItem multi times
        total_order = 0
        for order_item in order_items:
            oi = OrderDetail.objects.create(order = order, **order_item)
            oi.subtotal = oi.menu_resto.price * oi.quantity
            oi.status = StatusModel.objects.first()
            total_order += oi.subtotal
            oi.user_create = order.user_create
            oi.save()
        
        # Update the TableResto into Occupied
        TableResto.objects.filter(id = order.table_resto.id).update(table_status = 'Terisi')

        # Save Order
        order.total_order = total_order
        order.tax_order = 0.12 * float(total_order)
        order.total_payment = order.total_order + order.tax_order
        order.user = order.user_create
        order.save()
        return order

class OrderSerializer(serializers.ModelSerializer):
    table_resto = serializers.CharField(source = 'table_resto.name', read_only = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_status', 'total_order', 
            'tax_order', 'total_payment', 'user_create')

class OrderInfoSerializer(serializers.ModelSerializer):
    table_resto = serializers.CharField(source = 'table_resto.name', read_only = True)
    order_order_detail = OrderDetailCreateSerializer(many = True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'table_resto', 'user', 'order_status', 'order_order_detail', 'total_order', 
            'tax_order', 'total_payment', 'user_create')
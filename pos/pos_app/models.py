from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# user model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_waitress = models.BooleanField(default=False)
    
# Table Resto model
class TableResto(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )

    status_table_choices = (
        ('Kosong', 'Kosong'),
        ('Terisi', 'Terisi'),
    )

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    table_status = models.CharField(max_length=15, choices=status_table_choices, default='Kosong')
    status = models.CharField(max_length=15, choices=status_choices, default='Aktif')
    user_created = models.ForeignKey(User, related_name='user_created_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
    user_updated = models.ForeignKey(User, related_name='user_updated_table_resto', blank=True, null=True, on_delete=models.SET_NULL)
    create_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # user_created = models.CharField(max_length=100, blank=True, null=True)
    # user_updated = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Status Model
class StatusModel(models.Model):
    status_choices = (
        ('Aktif','Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
	) 
    name = models.CharField(max_length = 50, unique = True)
    description = models.TextField(blank = True, null = True)
    status = models.CharField(max_length = 15, 
        choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, 
        related_name = 'user_create_status_model', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, 
        related_name = 'user_update_status_model', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)


#kategori model
class Category(models.Model):
    name = models.CharField(max_length = 100)
    status = models.ForeignKey(StatusModel, related_name = 'status_category', on_delete = models.PROTECT)
    user_create = models.ForeignKey(User, related_name = 'user_create_category',
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_category',
        blank = True, null = True, on_delete = models.SET_NULL)

    # created_on = models.DateTimeField(blank = True, null = True)
    # last_modified = models.DateTimeField(blank = True, null = True)

    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

# Menu Resto
class MenuResto(models.Model):
    status_menu_choices = (
        ('Ada','Ada'),
        ('Habis', 'Habis'),
	) 
    code = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.CharField(max_length = 200)
    image_menu = models.ImageField(default = None, upload_to = 'menu_images/', blank = True, null = True)
    category = models.ForeignKey(Category, related_name = 'category_menu', blank = True, null = True, on_delete = models.SET_NULL)
    menu_status = models.CharField(max_length = 15, choices = status_menu_choices, default = 'Ada')
    status = models.ForeignKey(StatusModel, related_name = 'status_menu', on_delete = models.PROTECT)
    user_create = models.ForeignKey(User, related_name = 'user_create_menu', blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_menu', blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(blank = True, null = True)
    last_modified = models.DateTimeField(blank = True, null = True)
    
    # created_on = models.DateTimeField(auto_now_add = True)
    # last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']


def increment_order_code():
    last_code = Order.objects.all().last()

    if not last_code:
        return '0001' + '-' + str(datetime.today().month) + str(datetime.today().year)
    code = last_code.code
    code_int = int(code[0:4])
    new_code_int = code_int + 1
    return str(new_code_int).zfill(4) + '-' + str(datetime.today().month) + str(datetime.today().year)

class Order(models.Model):
    status_order_status_choices = (
        ('Belum Bayar','Belum Bayar'),
        ('Sudah Bayar', 'Sudah Bayar'),
	) 
    code = models.CharField(max_length = 20, default = increment_order_code, editable = False)
    table_resto = models.ForeignKey(TableResto, related_name = 'table_resto_order', 
        blank = True, null = True, on_delete = models.SET_NULL)    
    user = models.ForeignKey(User, related_name = 'user_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    order_status = models.CharField(max_length = 20, choices = status_order_status_choices, 
        default = 'Belum Bayar')
    total_order = models.FloatField(default = 0, blank = True, null = True)
    tax_order = models.FloatField(default = 0, blank = True, null = True)
    total_payment = models.FloatField(default = 0, blank = True, null = True)
    user_create = models.ForeignKey(User, related_name = 'user_create_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_order', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def _str_(self):
        return f'{self.code}'
    
class OrderDetail(models.Model):    
    status_order_detail_choices = (
        ('Sedang disiapkan','Sedang disiapkan'),
        ('Sudah disajikan', 'Sudah disajikan'),
	)
    order = models.ForeignKey(Order, related_name = 'order_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    menu_resto = models.ForeignKey(MenuResto, related_name = 'menu_resto_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default = 0)
    subtotal = models.IntegerField(default = 0, blank = True, null = True)
    description =  models.CharField(max_length = 200, blank = True, null = True)
    order_detail_status = models.CharField(max_length = 30, 
        choices = status_order_detail_choices, default = 'Sedang disiapkan')
    status = models.ForeignKey(StatusModel, related_name = 'status_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_create = models.ForeignKey(User, related_name = 'user_create_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_order_detail', 
        blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def _str_(self):
        return f'{self.order}'
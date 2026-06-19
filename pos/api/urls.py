from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
  RegisterUserAPIView, LoginView, LogoutView, TableRestoListApiView, TableRestoDetailApiView, MenuRestoView, MenuRestoFirterApi, MenuRestoPermissionView, get_csrf,CategoryView
)

app_name = 'api'
urlpatterns = [
  path('api/register', RegisterUserAPIView.as_view()),
  path('api/login', LoginView.as_view()),
  path('api/logout', LogoutView.as_view()),
  
  

  path('api/table-resto', views.TableRestoListApiView.as_view()),
  path('api/table-resto/<int:id>', views.TableRestoDetailApiView.as_view()),

  path('api/menu-resto-list', views.MenuRestoView.as_view()),
  path('api/menu-resto-filter/', views.MenuRestoFirterApi.as_view()),
  
  path('api/category-list', views.CategoryView.as_view()),

  #menu resto with permision
  path('api/menu-resto', views.MenuRestoPermissionView.as_view()),

  path('api/get-csrf/', views.get_csrf),
  
  path('api/order-list', views.OrderListApiView.as_view()),
  path('api/order-create', views.OrderCreateApiView.as_view()),
  path('api/order-info/<pk>', views.OrderInfoApiView.as_view()),
  path('api/order-delete/<pk>', views.OrderDeleteApiView.as_view()),

]

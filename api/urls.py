from django.urls import path
from . import views
from .views import RegisterApi, Login

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('api/login/', Login.as_view()),
      path('user/update/', views.UpdateUser.as_view(), name='user_update'),
      path('shop/create/', views.ShopView.as_view(), name='shop_create'),
      path('shop/get/', views.GetShopView.as_view(), name='shop_get'),

]


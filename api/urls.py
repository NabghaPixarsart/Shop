from django.urls import path
from . import views
from .views import RegisterApi, Login

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('api/login/', Login.as_view()),
      path('user/update/', views.UpdateUser.as_view(), name='user_update'),
      path('shop/create/', views.ShopView.as_view(), name='shop_create'),
      path('user/shop/', views.ShopApi.as_view(), name='shop_update'),
      path('shop-list/', views.UserShopView.as_view(), name='shop-list'),
      # path('update/', RegisterShopView.as_view(), name='update_shop'),
      # path('user/id/shop/', views.ShopUserApi.as_view(), name='shop_id'),

]

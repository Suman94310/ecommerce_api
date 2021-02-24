from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from products import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<int:pk>/', views.ProductsDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('tokenToUser/', views.TokenToUser.as_view()),
    path('getUsers/', views.UserDetail.as_view()),
    path('register/', views.CreateUser.as_view()),
    path('createItems/', views.ItemCreate.as_view()),
    path('updateItems/', views.ItemUpdate.as_view()),
    path('ListItems/', views.ItemList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
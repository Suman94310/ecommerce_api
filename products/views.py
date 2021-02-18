from rest_framework import mixins
from rest_framework import generics
from products.models import Products, Item
from products.serializers import ProductsSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer, ItemSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters



# authorization
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class ProductsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = Products.objects.all()
        bought = self.request.query_params.get('bought', None)
        if bought is not None:
            queryset = queryset.filter(bought=bought)
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductsDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['owner']
    filter_backends = (filters.SearchFilter,)
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ItemList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    serializer_class =ItemSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Item.objects.all()
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tag=tag)
        return queryset

class ItemCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Item.objects.all()
    serializer_class =ItemSerializer

class ItemUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Item.objects.all()
    serializer_class =ItemSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        temp = Products.objects.filter(owner=Token.objects.get(key=request.data['token']).user.id)
        return Response(temp)

class TokenToUser(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        temp1 = Token.objects.get(key=request.data['token']).user.id
        temp2 = Token.objects.get(key=request.data['token']).user.username
        return Response({'id': temp1, 'username': temp2})

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer





@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
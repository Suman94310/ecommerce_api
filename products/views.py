from rest_framework import mixins
from rest_framework import generics
from products.models import Products, Item
from products.serializers import ProductsSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegistrationSerializer, ItemSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class ProductsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductsDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    serializer_class =ItemSerializer
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
    queryset = Item.objects.all()
    serializer_class =ItemSerializer

class ItemUpdate(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class =ItemSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
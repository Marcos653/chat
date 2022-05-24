from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import *
from .serializers import *
from django.db.models import Q, Count
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            if user.active == True:
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                        'token': token.key,
                        'type_user': user.type_user,
                    })
            else:
                
               return Response({"message": "User is disabled!"}, status=status.HTTP_400_BAD_REQUEST)  

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['post'], url_path='change-forgotten-password', permission_classes=[AllowAny])
    def change_forgotten_password(self, request):
        email = request.POST.get('email', None)
        forgot_password_hash = request.POST['forgot_password_hash']
        new_password = request.POST['new_password']
        User.change_password(email, forgot_password_hash, new_password)
        return Response({'worked': True})

    @action(detail=False, methods=['get'], url_path='filter')
    def get_filter_user(self, request):
        name = request.query_params.get('name', None)
        email = request.query_params.get('email', None)

        if name:
            queryset = self.queryset.filter(name__icontains=name)
            page = self.paginate_queryset(queryset)
            serializer = UserSerializer(page, many=True)

            return self.get_paginated_response(serializer.data, )

        elif email:
            queryset = self.queryset.filter(email__icontains=email)
            page = self.paginate_queryset(queryset)
            serializer = UserSerializer(page, many=True)

            return self.get_paginated_response(serializer.data, )
        else:

            return Response({"message": "Not found!"})


    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(user, many=True).data

        if len(serializer) == 1:
            serializer = serializer[0]
        return Response(serializer)
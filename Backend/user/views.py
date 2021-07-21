from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithToken
)
from user.utils import IsAdminOrAgent

UserModel = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerAgent(request):
    """
    register agent type user
    """
    data = request.data
    try:
        user = UserModel.objects.create_agent(
            username=data.get('username'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        user.save()
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail': 'User with this email alrady exists.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerCustomer(request):
    """
    register customer type user
    """
    data = request.data
    try:
        user = UserModel.objects.create_customer(
            username=data.get('username'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        user.save()
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail': 'User with this email alrady exists.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrAgent])
def get_user_list(request, *args, **kwargs):
    """
    get list of users according to hierarchy of admin and agent. From point 1.
    """
    if request.user.user_type == 'admin':
        customer = UserModel.customermanager.all()
        agent = UserModel.agentmanager.all()
        query = customer.union(agent)
        serializer = UserSerializer(query, many=True)
    if request.user.user_type == 'agent':
        customer = UserModel.customermanager.all()
        serializer = UserSerializer(customer, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, AllowAny])
def get_user_view(request, id, *args, **kwargs):
    """
    get user detail views also according to hierarchy of user. From point 1.
    """
    user = UserModel.objects.get(pk=id)
    if user != request.user:
        if request.user.user_type == 'admin' and user.user_type == 'admin':
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'agent' and (
            user.user_type == 'admin' or user.user_type == 'agent'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'customer' and (
            user.user_type == 'customer' or user.user_type == 'admin' or user.user_type == 'agent'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrAgent])
def get_user_edit(request, id, *args, **kwargs):
    """
    get edit of user according to hierarchy of admin and agent. From point 1.
    """
    data = request.data
    user = UserModel.objects.get(pk=id)
    if user != request.user:
        if request.user.user_type == 'admin' and user.user_type == 'admin':
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)
        if request.user.user_type == 'agent' and (
            user.user_type == 'admin' or user.user_type == 'agent'
        ):
            return Response({'message': 'Not Allowed'}, status=HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)
    try:
        serializer.update(instance=user, validated_data=data)
    except Exception as e:
        return Response(
            {'message': 'Invalid Entry.'},
            status=HTTP_304_NOT_MODIFIED
        )
    return Response(serializer.data, status=HTTP_200_OK)

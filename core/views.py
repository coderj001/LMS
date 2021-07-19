from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.models import Loan
from core.serializers import LoanSerializers
from user.models import User
from user.utils import (
    IsAdmin,
    IsAdminOrAgent,
    IsAgent
)


# yyyy/mm/dd
def set_date(sdate):
    var = list(map(int, sdate.split('/')))
    return datetime(var[0], var[1], var[2])


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAgent])
def request_loan(request, *args, **kwargs):
    agent = request.user
    data = request.data
    try:
        customer = User.customermanager.get(username=data.get('customer'))
        loan = Loan.objects.create(
            amount=int(data.get('amount')),
            start_date=set_date(data.get('start_date')),
            duration=int(data.get('duration')),
            interest_rate=float(data.get('interest_rate')),
            customer=customer,
            agent=agent
        )
        loan.save()
        serializer = LoanSerializers(loan)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail': 'Invalid Parameters.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAgent])
def edit_loan(request, *args, **kwargs):
    agent = request.user
    data = request.data
    try:
        loan = Loan.objects.get(pk=kwargs.get('id'))
        if agent == loan.agent:
            if loan.status == 'new':
                customer = User.customermanager.get(
                    username=data.get('customer'))
                loan.amount = int(data.get('amount'))
                loan.start_date = set_date(data.get('start_date'))
                loan.duration = int(data.get('duration'))
                loan.interest_rate = float(data.get('interest_rate'))
                loan.customer = customer
                loan.save()
                serializer = LoanSerializers(loan)
                return Response(serializer.data)
            else:
                message = {'detail': 'Can\'t edit.'}
                return Response(message, status=HTTP_400_BAD_REQUEST)
        else:
            message = {'detail': 'You don\'t have right to edit.'}
            return Response(message, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = {'detail': 'Invalid Parameters.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)


# TODO:  <30-06-21, coderj001> # only
@api_view(['GET'])
@permission_classes([IsAuthenticated, AllowAny])
def list_loan(request, *args, **kwargs):
    user = request.user
    status = request.query_params.get('status')
    created_at = request.query_params.get('created_at')

    if user.user_type == 'admin':
        loan = Loan.objects.all().order_by('updated_at')
    if user.user_type == 'agent':
        loan = user.user_agent.all().order_by('updated_at')
    if user.user_type == 'customer':
        loan = user.user_customer.all().order_by('updated_at')

    if status:
        loan = loan.filter(status=status)
    if created_at:
        loan = loan.filter(created_at=set_date(created_at))

    serializer = LoanSerializers(loan, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def request_loan_approved(request, *args, **kwargs):
    try:
        loan = Loan.objects.get(pk=kwargs.get('id'))
    except Loan.DoesNotExist:
        message = {'error': f'User with {kwargs.get("id")} not found.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
    loan.status = 'approved'
    loan.save()
    message = {'success': 'Loan is approved.'}
    return Response(message, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def request_loan_rejected(request, *args, **kwargs):
    try:
        loan = Loan.objects.get(pk=kwargs.get('id'))
    except Loan.DoesNotExist:
        message = {'error': f'User with {kwargs.get("id")} not found.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
    loan.status = 'rejected'
    loan.save()
    message = {'success': 'Loan is rejected.'}
    return Response(message, status=HTTP_200_OK)

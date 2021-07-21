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
    """
    Create loan by only agent type user. From point 2.
    """
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
    """
    Edit loan by only agent type user. From point 4.
    """
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
    """
    Get list of loan according to hierarchy of users. From point 2.
    """
    user = request.user
    status = request.query_params.get('status')
    created_at = request.query_params.get('created_at')
    updated_at = request.query_params.get('updated_at')

    if user.user_type == 'admin':
        loan = Loan.objects.all().order_by('updated_at')
    if user.user_type == 'agent':
        loan = user.user_agent.all().order_by('updated_at')
    if user.user_type == 'customer':
        loan = user.user_customer.all().order_by('updated_at')

    if status:
        loan = loan.filter(status=status)
    if created_at:
        dt = set_date(created_at)
        loan = loan.filter(
            created_at__year=dt.year,
            created_at__month=dt.month,
            created_at__day=dt.day
        )
    if updated_at:
        dt = set_date(updated_at)
        loan = loan.filter(
            updated_at__year=dt.year,
            updated_at__month=dt.month,
            updated_at__day=dt.day
        )

    serializer = LoanSerializers(loan, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def request_loan_approved(request, *args, **kwargs):
    """
    Approval loan only by admin user. From point 3.
    """
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
    """
    Reject loan only by admin user. From point 3.
    """
    try:
        loan = Loan.objects.get(pk=kwargs.get('id'))
    except Loan.DoesNotExist:
        message = {'error': f'User with {kwargs.get("id")} not found.'}
        return Response(message, status=HTTP_400_BAD_REQUEST)
    loan.status = 'rejected'
    loan.save()
    message = {'success': 'Loan is rejected.'}
    return Response(message, status=HTTP_200_OK)

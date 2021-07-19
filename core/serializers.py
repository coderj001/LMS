from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Loan
from user.models import User


class LoanSerializers(ModelSerializer):
    agent = SerializerMethodField(read_only=True)
    customer = SerializerMethodField()

    class Meta:
        model = Loan
        fields = (
            'id',
            'amount',
            'interest_rate',
            'start_date',
            'duration',
            'status',
            'emi',
            'agent',
            'customer'
        )

    def get_agent(self, obj):
        return obj.agent.username

    def get_customer(self, obj):
        return obj.customer.username

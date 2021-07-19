from django.contrib import admin
from core.models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'status',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'status',
        'created_at',
        'updated_at'
    )

from django.urls import path

from core.views import (
    request_loan,
    list_loan,
    edit_loan,
    request_loan_approved,
    request_loan_rejected
)

app_name = "core"

urlpatterns = [
    path('create/', request_loan, name="create_loan"),
    path('list/', list_loan, name="list_loan"),
    path('edit/<int:id>/', edit_loan, name="edit_loan"),
    path('<int:id>/approved/', request_loan_approved, name="approved_loan"),
    path('<int:id>/rejected/', request_loan_rejected, name="rejected_loan"),
]

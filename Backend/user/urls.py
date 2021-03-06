from django.urls import path

from user.views import (
    MyTokenObtainPairView,
    get_user_edit,
    get_user_list,
    get_user_view,
    registerAgent,
    registerCustomer
)

app_name = "user"

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name="user_login"),
    path('register/agent/', registerAgent, name="agent_register"),
    path('register/customer/', registerCustomer, name="customer_register"),
    path('list/', get_user_list, name="user_list"),
    path('<uuid:id>/', get_user_view, name="user_view"),
    path('<uuid:id>/edit/', get_user_edit, name="user_edit"),
]

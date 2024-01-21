from django.urls import path
from user import views

# User for reverse mapping in test
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
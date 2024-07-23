from django.urls import path
from .views import RegisterUserAPIView, LoginAPIView, ProtectedExampleView, UserView,LogoutAPIView,CategoryView,ChangePasswordView

urlpatterns = [
  # This code block is defining URL patterns for a Django application. Each `path` function call maps
  # a URL pattern to a specific view class. Here's a breakdown of what each line is doing:
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('transactions/', ProtectedExampleView.as_view(), name='protected'),
    path('insert/', ProtectedExampleView.as_view(), name='protected'),
    path('update/', ProtectedExampleView.as_view(), name='protected'),
    path('remove/<int:pk>/', ProtectedExampleView.as_view(), name='protected-delete'),
    path('user/', UserView.as_view(), name='userView'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('categories/', CategoryView.as_view(), name='protected'),
    path('insertCategory/', CategoryView.as_view(), name='protected'),
    path('updateCategory/', CategoryView.as_view(), name='protected'),
    path('removeCategory/<int:pk>/', CategoryView.as_view(), name='protected-delete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView 

urlpatterns = [
    path("signup", SignUpView.as_view(template_name = "templates/registrar.html"), name = "signup")
]

from django.conf.urls import url
from app.views import SignupView,LoginView,LogoutView
urlpatterns = [
    url(r'Signup',SignupView.as_view()),
    url(r'Login',LoginView.as_view()),
    url(r'Logout',LogoutView.as_view())
]

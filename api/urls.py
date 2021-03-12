from django.urls import path

from .views import (
    UserView,
    BookingView,
    EventView,
    RegisterView,
    LoginAPI,
    UserAPI,
)

from knox import views as knox_views


urlpatterns = [
    path("bookings/", BookingView.as_view()),
    path("user/", UserView.as_view()),
    path("events/", EventView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/logout/", knox_views.LogoutView.as_view()),
    path("auth/getuser/", UserAPI.as_view()),
]

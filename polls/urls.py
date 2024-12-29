from polls.views import *
from django.urls import path


urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path("users/",UserListView.as_view())
]
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.models import User


class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('users:register_success')
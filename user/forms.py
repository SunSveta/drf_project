from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from forms_mixins import StyleFormMixin
from user.models import User


class CustomEditUserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.forms import ModelMultipleChoiceField

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'
        groups = ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

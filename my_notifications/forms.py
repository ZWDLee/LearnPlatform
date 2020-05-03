from django import forms
from .models import SystemNotification


class SystemNotificationForm(forms.ModelForm):

    class Meta:
        model = SystemNotification
        fields = '__all__'

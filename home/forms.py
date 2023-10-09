from django import forms
from .models import CustomerSupportRequest

class CustomerSupportRequestForm(forms.Form):
    model = CustomerSupportRequest
    fields = ['client_ip', 'room_slug']

    def clean(self):
        if self.is_valid():
            client_ip = self.cleaned_data['client_ip']
            room_slug = self.cleaned_data['room_slug']
        return self.cleaned_data

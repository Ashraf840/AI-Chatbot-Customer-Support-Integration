from django import forms
from .models import CustomerSupportRequest

class CustomerSupportRequestForm(forms.Form):
    model = CustomerSupportRequest
    fields = ['client_ip', 'room_slug']

    def clean(self):
        # NB: use this func in order to make custom-validation of each/certain field(s)
        if self.is_valid():
            client_ip = self.cleaned_data['client_ip']
            room_slug = self.cleaned_data['room_slug']
        return self.cleaned_data

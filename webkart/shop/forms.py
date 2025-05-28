from django import forms
from .models import Contact
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "desc"]
        labels = {
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "desc": "How May We Help You?"
        }
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 5})
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit():
            raise ValidationError("Must contain only numbers")
        elif len(phone) < 10:
            raise ValidationError("Must be 10 digits")
        return phone
    
    def send_mail(self):
        print(f"sending email from {self.cleaned_data["email"]} with message: {self.cleaned_data["desc"]}")
        
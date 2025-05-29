from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
# from django.contrib import messages


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "subject", "desc"]
        labels = {
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "subject": "Subject",
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
    
    def send_email(self, request):
        cleaned_data = super().clean()
        send_mail(
            subject = f"New Contact Form Submission: {cleaned_data.get('subject')}",
            message = f"New message received\n\nName: {cleaned_data.get('name')}\nEmail: {cleaned_data.get('email')}\nMessage: {cleaned_data.get('desc')}",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [settings.EMAIL_HOST_USER],
            fail_silently = False
        )

        send_mail(
            subject = "Thank you for contacting WebKart",
            message = f"Hi {cleaned_data.get('name')},\n\nThank you for contacting us.\nWe have received your message and will respond within 24 hours.\n\n- Team WebKart",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [self.cleaned_data["email"]],
            fail_silently = False
        )

        # messages.success(request, f"Thank you {cleaned_data.get('name')}, your message has been received!")

from django import forms
from .models import Ticket
from django.contrib.auth.models import User, Group


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'file']  # Fayl maydoni qo'shildi


class ITSpecialistSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            group = Group.objects.get(name='IT Mutaxassis')
            user.groups.add(group)
        return user

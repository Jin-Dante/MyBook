from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book


class BookForm(forms.ModelForm):
    # Accepts two date formats: DD-MM-YYYY and YYYY-MM-DD
    published_date = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'], label="Published Date")
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'description', 'pdf', 'image','available']

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username'}) # Adds a placeholder for the username field
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}) # Adds a placeholder for the email field
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Specifies the fields to be included in the registration form

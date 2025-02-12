from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes all required fields plus
    additional profile information.
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all fields on the user model
    except the password field.
    """
    password = None  # Remove password field from the form
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'bio',
                 'birth_date', 'avatar', 'location', 'website',
                 'twitter', 'linkedin', 'github')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating user profile information only.
    """
    class Meta:
        model = get_user_model()
        fields = ('bio', 'birth_date', 'avatar', 'location', 'website',
                 'twitter', 'linkedin', 'github')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
from django import forms
from .models import Course,Rating
from django.contrib.auth.models import User



class RatingForm(forms.Form):
    rating = forms.IntegerField(
        label='Rate this course (0-10)', 
        min_value=0, 
        max_value=10,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a rating between 0 and 10'})
    )
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description'] 
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return password_confirmation
    

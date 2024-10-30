from django import forms
from .models import Problem


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'title',
            'description',
            'image',
            'note',
            'examples',
            'theme',
            'algorithm',
            'difficulty',
            'solution'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'note': forms.Textarea(attrs={'rows': 3}),
            'solution': forms.Textarea(attrs={'rows': 6}),
        }

from django import forms
from .models import Recipe
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 1,
                'style': 'height: 36px; resize: vertical; padding: 8px; border-radius: 6px; width: 100%;',
                'placeholder': 'Write a comment...',
            }),
            'rating': forms.Select(attrs={
                'style': 'height: 36px; border-radius: 6px;'
            })
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients','steps','description', 'image']

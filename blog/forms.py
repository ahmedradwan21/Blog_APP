from django import forms
from .models import BlogPost
from .models import Category

class BlogPostForm(forms.ModelForm):
    PUBLISH_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    publish_status = forms.ChoiceField(
        label="Publish Status",
        choices=PUBLISH_CHOICES,
        widget=forms.RadioSelect(),
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  
    )
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'publish_status', 'categories']

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
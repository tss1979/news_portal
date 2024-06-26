from django import forms
from .models import Post, Category


class SubscribeForm(forms.Form):
    def __int__(self, *args, **kwags):
        self.fields['category'].empty_label = None

    category = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
    )

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwags):
        super().__init__(*args, **kwags)
        self.fields['author'].empty_label = 'Not'
        self.fields['category'].empty_label = None

    class Meta:
       model = Post
       fields = [
           'author',
           'category',
           'title',
           'text',
       ]
       widgets = {
           'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
           'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
           'category': forms.CheckboxSelectMultiple(),
       }




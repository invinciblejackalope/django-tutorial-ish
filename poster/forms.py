from django import forms

# form to create posts
class PostForm(forms.Form):
    # form fields (the labels are used to render the form)
    text = forms.CharField(label='Text', max_length=1000)
    author = forms.CharField(label='Author', max_length=100)

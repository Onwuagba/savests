from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
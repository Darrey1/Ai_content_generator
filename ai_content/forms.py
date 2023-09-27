from django import forms
class Youtube(forms.Form):
    search = forms.CharField(max_length=100, label='Search:', required=True)
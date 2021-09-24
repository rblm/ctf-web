from django import forms

class DlForm(forms.Form):
    CHOICES=(
            ('passwords','passwords'),
            ('flag','flag'),
            ('classified','classified docs'),
            )
    password = forms.CharField(label='password',max_length=32)
    pin = forms.CharField(label='pin',max_length=32)
    files = forms.ChoiceField(choices=CHOICES)

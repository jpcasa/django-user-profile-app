from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput())
    confirm_email=forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'bio',
            'city',
            'state',
            'country',
            'favorite_animal',
            'hobby',
        ]

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email != confirm_email:
            raise forms.ValidationError(
                "Emails must match!"
            )

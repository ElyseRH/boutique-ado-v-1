from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # render all fields except user, coz that should never change
        exclude = ('user',)

    # override init method
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # call init, then create dict with nicer looking labels
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
        }

        # autofocus means cursor will start here, then iterate through fields
        # include check for country
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'  # this adds * if required
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder  # this sets placeholders to their values set in the dict above
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'  # adds a custom css class
            self.fields[field].label = False  # removes form fields labels, as we added our own
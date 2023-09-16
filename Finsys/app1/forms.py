from django import forms
from .models import *
from .models import noninventory
from .models import BankAccountHolder, BankAccount, BankConfiguration, MailingAddress, BankingDetails, OpeningBalance


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = service
#         fields = ['img', 'name', 'sku', 'sac', 'unit','categ','descr','check1','saleprice','income','check2','tax','abatement','sertype']


# class ImageForm2(forms.ModelForm):
#     class Meta:
#         model=noninventory
#         fields=("image","name","sku","hsn","unit","category","initialqty","date","stockalrt","invacnt","description","salesprice","incomeacnt","tax","purchaseinfo","cost","expacnt","purtax","revcharge","presupplier",)


class ImageForm3(forms.ModelForm):
    class Meta:
        model = bundle
        fields = ['image', 'name', 'sku', 'description']

class ImageForm4(forms.ModelForm):
    class Meta:
        model=inventory
        fields=("image","name","sku","hsn","unit","category","initialqty","date","stockalrt","invacnt","description","salesprice","incomeacnt","tax","purchaseinfo","cost","expacnt","purtax","revcharge","presupplier")


class BankAccountHolderForm(forms.ModelForm):
    class Meta:
        model = BankAccountHolder
        fields = ['name', 'alias', 'phone_number', 'email', 'account_type']
        labels = {
            'name': 'Name',
        }
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        
        fields = ['holder_name', 'account_number', 'ifsc_code', 'swift_code', 'bank_name', 'branch_name']
        widgets = {
            'bank_name': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class MailingAddressForm(forms.ModelForm):
    class Meta:
        model = MailingAddress
        fields = ['mailing_name', 'address', 'country', 'state', 'pin']  
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        
        
class OpeningBalanceForm(forms.ModelForm):
    class Meta:
        model = OpeningBalance
        fields = ['date', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class BankingDetailsForm(forms.ModelForm):
    set_alter_gst_details = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select)

    class Meta:
        model = BankingDetails
        fields = ['pan_it_number', 'registration_type', 'gstin_un', 'set_alter_gst_details']
        labels = {
            'registration_type': 'Registration Type',
        }
        widgets = {
            # Set the id attribute for the registration type and GST number fields
            'registration_type': forms.Select(attrs={'id': 'id_registration_type'}),
            'gstin_un': forms.TextInput(attrs={'id': 'id_gstin_un'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        registration_type = cleaned_data.get('registration_type')
        if registration_type in ['consumer', 'unregistered']:
            # Skip validation for the GST number field
            if 'gstin_un' in self.errors:
                del self.errors['gstin_un']
        return cleaned_data
        
        
class BankConfigurationForm(forms.ModelForm):
    set_cheque_book_range = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select)
    enable_cheque_printing = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select)
    set_cheque_printing_configuration = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select)

    class Meta:
        model = BankConfiguration
        fields = ['set_cheque_book_range', 'enable_cheque_printing', 'set_cheque_printing_configuration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-control', 'data-placeholder': field.label})
        
        
class BankAccountFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'All'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-control', 'data-placeholder': field.label})
from django import forms

from .models import Expenses

class expenseApprovalForm(forms.ModelForm):
    hotel_rent = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    transport = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    meal = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    travel_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Travel Date'}))
    airfare = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    others = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    remarks = forms.Textarea()
    class Meta:
        model = Expenses
        exclude = ['employee','form_status','total_amount', 'department']
from django import forms
from .models import excelData

class UploadFileForm(forms.ModelForm):
    class Meta: 
        model = excelData
    
        fields = ('file' , )


class MALIYET(forms.Form):
    product_cost = forms.TextInput
    warehouse_cost = forms.TextInput
    order_id = forms.CharField

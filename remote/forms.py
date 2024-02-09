from django import forms
from .models import excelData

class UploadFileForm(forms.ModelForm):
    class Meta: 
        model = excelData
    
        fields = ('com_asin' , 'target_asin' ,)
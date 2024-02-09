from django import forms 
from .models import OrderFileData

class UploadFileForm(forms.ModelForm):
    class Meta: 
        model = OrderFileData
    
        fields = ('file' , )
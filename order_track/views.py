from django.shortcuts import render
from .order_track import order_track
from .forms import UploadFileForm
from .fileupload import uploaded_file
from main.models import Fransa

def kargotakip(request):
   
    apiKey = "w7xxm92y-c73w-k4ip-l6we-yhufw5dtw51g"
    order_list = order_track(apiKey=apiKey)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file(request.FILES['file'] , Fransa)
    else:
        form = UploadFileForm()
    data = {        
            "info" : order_list , 
            'form' : form
        }
    return render(request , "kargotakip.html" , data)
    


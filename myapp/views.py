from django.shortcuts import render,HttpResponse
import img2pdf
from PIL import Image,ImageOps
import os
import uuid
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import datetime
# Create your views here.

def index(request):
    data = []
    pdf_path = None
    temp_path = None
    if request.method == "POST":
        images_list = []
        file_name = request.POST.get("filename")
        path = os.path.join(settings.BASE_DIR,"user_generated")
        path = os.path.join(path,file_name)
        # splitted_name = file_name.split('.')[0]
        date = datetime.datetime.now()
        my_date = date.strftime("%Y%m%d%H %M%S%f")
        date_str = str(my_date)
        pdf_path = f"{file_name}{date_str}.pdf" 
        pdf_path = os.path.join(path,pdf_path)
        if not os.path.exists(path):
            os.mkdir(path)

        for item in request.FILES.getlist("images"):
            filename = item.name
            # print(filename)
            filename = os.path.join(path,filename)
            with open(filename, "wb") as f:
                f.write(item.read())

            image = Image.open(filename)
            im = ImageOps.grayscale(image)
            images_list.append(image)
                    
        images_list[0].save(pdf_path,"PDF",save_all=True,append_images=images_list[1:])
        # return HttpResponse("Done")  
        return FileResponse(open(pdf_path,'rb'),content_type="application/pdf")
            
    return render(request,'index.html')


    
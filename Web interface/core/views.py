import requests
from django.shortcuts import render, redirect
from .forms import *

def handle_uploaded_file(f):
    print("handling")
    #with open("some/file/name.txt", "wb+") as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)



def is_url_image(image_url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
        return False
    except:
        return False


# Запускается после отпрвки картинки или видео
def url_page(request):

    form = InputUrlForm()
    fform = InputFileForm()

    if request.method == "POST":

        form = InputUrlForm(request.POST)
        fform = InputFileForm(request.POST)
        # ссылка на картинку c с квадратиком, можно ссылку файлом
        image_classified_url = None
        # 0 Если оружия нет 1 если есть
        image_danger_status = 0

        #Если отправлена ссылка
        if form.is_valid():
            #Считывание ссылки и проверка на существование
            fform = InputFileForm()
            image_classified_url = form.cleaned_data["url"]
            if not is_url_image(image_classified_url):
                form = InputUrlForm(initial = {'url' : 'bad url'})
                return render(request, "frontpage.html", {"form": form, "fform" : fform})
            
            #
            # image_classified_url = 
            #

        #Если отправлен файл
        elif fform.is_valid():
            form = InputUrlForm()
            image_classified_url = fform.cleaned_data["file"]
            print(image_classified_url)

        #Если ниче не отправили
        return render(request, "frontpage.html", {"form": form, "fform" : fform, "url" : image_classified_url})
            
    return render(request, "frontpage.html", {"form": form, "fform" : fform})

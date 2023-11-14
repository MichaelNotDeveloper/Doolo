import requests
from django.shortcuts import render, redirect
from .forms import *
from .weapon_detector import *
import random
import os

IMAGES_FILEPATH = "core/static/"
IMAGES_AMOUNT = 5
weapon_detector = WeaponDetector('weights/best.pt')


# Грузит файлик в files/{filename}.{filetype}
def handle_uploaded_file(f):
    with open(IMAGES_FILEPATH + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Проверка что ссылка существует и соответсвует форматам
def url_works(image_url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg", "image/mp4")
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
        fform = InputFileForm(request.POST, request.FILES)
        # ссылка на изначалбную картинку
        image_url = None
        # 1 Если оружия нет 2 если есть
        image_classified_type = None

        #Если отправлена ссылка
        if form.is_valid():
            #Считывание ссылки и проверка на существование
            fform = InputFileForm()
            image_url = form.cleaned_data["url"]
            
            if not url_works(image_url):
                form = InputUrlForm(initial = {'url' : 'bad url'})
                return render(request, "frontpage.html", {"form": form, "fform" : fform})
            
            # ссылка на картинку с квадратиком, можно имя файлом лежащим в IMAGES_FILEPATH (Тут кодит арсений)
            
            img_data = requests.get(image_url).content
            filetype = '.' + image_url.split('.')[-1]
            image_url = IMAGES_FILEPATH + f'image0' + filetype

            with open(image_url, 'wb') as handler:
                handler.write(img_data)

            image_classified_url = image_url
            image_classified_type = int(weapon_detector.Process(image_url, IMAGES_FILEPATH)) + 1
            #

        #Если отправлен файл
        else:
            form = InputUrlForm()
            # Сохраняем файл в IMAGES_FILEPATH, имя не меняем
            file = request.FILES['file']
            filename = request.FILES['file'].name
            image_url = IMAGES_FILEPATH + filename
            handle_uploaded_file(file)
            # predict 
            image_classified_type = int(weapon_detector.Process(image_url, IMAGES_FILEPATH)) + 1
            #удаляем файлик
            os.remove(image_url.replace(' ', '\ '))
            #

        image_names = [f"image{i+1}.jpg" for i in range(IMAGES_AMOUNT)]
        return render(request, "frontpage.html", {"form": form, "fform" : fform, "showtype" : image_classified_type, "images" : image_names})
    
    return render(request, "frontpage.html", {"form": form, "fform" : fform})

import requests
from django.shortcuts import render, redirect
from .forms import *

IMAGES_FILEPATH = "core/static/"

# Грузит файлик в files/{filename}.{filetype}
def handle_uploaded_file(f):
    with open(IMAGES_FILEPATH + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Проверка что ссылка существует и соответсвует форматам
def is_url_image(image_url):
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
        # ссылка на картинку с квадратиком, можно имя файлом лежащим в IMAGES_FILEPATH
        image_classified_url = None
        # Тип ссылки на картинку 0 - url, 1 - file, 2 - None
        image_classified_type = 2
        # 0 Если оружия нет 1 если есть
        image_danger_status = 0

        #Если отправлена ссылка
        if form.is_valid():
            #Считывание ссылки и проверка на существование
            fform = InputFileForm()
            image_url = form.cleaned_data["url"]
            if not is_url_image(image_url):
                form = InputUrlForm(initial = {'url' : 'bad url'})
                return render(request, "frontpage.html", {"form": form, "fform" : fform})
            
            # ссылка на картинку с квадратиком, можно имя файлом лежащим в IMAGES_FILEPATH (Тут кодит арсений)
            image_classified_url = image_url
            image_classified_type = 0
            #

        #Если отправлен файл
        else:
            form = InputUrlForm()
            # Сохраняем файл в IMAGES_FILEPATH, имя не меняем
            file = request.FILES['file']
            filename = request.FILES['file'].name
            handle_uploaded_file(file)
            image_url = IMAGES_FILEPATH + request.FILES['file'].name

            # ссылка на картинку с квадратиком, можно имя файлом лежащим в IMAGES_FILEPATH (Тут кодит арсений)
            image_classified_url = filename
            image_classified_type = 1
            #

            print(image_classified_url)
        return render(request, "frontpage.html", {"form": form, "fform" : fform, "url" : image_classified_url, "showtype" : image_classified_type})
    
    return render(request, "frontpage.html", {"form": form, "fform" : fform})

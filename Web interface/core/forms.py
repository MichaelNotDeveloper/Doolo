from django import forms

class InputUrlForm(forms.Form):
    url = forms.CharField(label = '', widget = forms.TextInput(attrs = {
        "class" : "text-field__input",
        "type" : "text",
        "placeholder" : "Image url:",
    }))

class InputFileForm(forms.Form):
    file = forms.FileField(label = "", widget = forms.FileInput( attrs = {"accept" : ".png,.jpg"}))

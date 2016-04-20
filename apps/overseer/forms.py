import json

from django import forms


class UploadJsonDataForm(forms.Form):

    json_file = forms.FileField()

    def clean_json_file(self):
        data = super(UploadJsonDataForm, self).clean()
        json_file = data.get('json_file')
        try:
            json_data = json.loads(json_file.read())
        except ValueError:
            raise forms.ValidationError('Could not convert data to JSON. '\
                    'Please make sure the file is a valid JSON file.')
        return data

    def save_data(self):
        data = self.cleaned_data
        json_file = data.get('json_file')
        json_data = json.loads(json_file.read())

        print json_data

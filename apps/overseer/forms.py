import json

from django import forms

from apps.overseer.tasks import CreateBulkInstitutes


class UploadJsonDataForm(forms.Form):

    file_data = None
    json_file = forms.FileField()

    def clean_json_file(self):
        data = super(UploadJsonDataForm, self).clean()
        json_file = data.get('json_file')
        try:
            json_data = json.loads(json_file.read())
            self.file_data = json_data
        except ValueError:
            raise forms.ValidationError('Could not convert data to JSON. '\
                    'Please make sure the file is a valid JSON file.')
        return json_file

    def save_data(self):
        if self.file_data:
            create_institutes = CreateBulkInstitutes()
            create_institutes.apply_async(args=(self.file_data, ))

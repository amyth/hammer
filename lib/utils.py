import json

from django.http import HttpResponse


def clean_string(x):
	x = x.lower()
	x = ' '.join(i.strip() for i in x.split())
	x = ''.join(i for i in x if i.isalnum())

	return x

def jsonresponse(json_data):
	return HttpResponse(json.dumps(json_data), content_type="application/json")
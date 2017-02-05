import json as libjson
from LicensesPlates import PlateReader
from django.http import HttpResponse
from django.template import RequestContext, loader


def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request)
    return HttpResponse(template._render(context))


def capturePlate(request):
    plate_reader = PlateReader.ReadPlates()
    response, errors = plate_reader.alpr_json_results()
    results = response.get('results')
    template = loader.get_template('check.html')
    context = RequestContext(request, {'plate': results[0].get('plate'), 'confidence': results[0].get('confidence')})
    return HttpResponse(template._render(context))

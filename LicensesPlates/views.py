from LicensesPlates import PlateReader
from django.shortcuts import render
from django.template import RequestContext

def home(request):
    context = RequestContext(request)
    return render(request, 'home.html')


def capturePlate(request):
    plate_reader = PlateReader.ReadPlates()
    response, errors = plate_reader.alpr_json_results()
    results = response.get('results')
    context = RequestContext(request, {'plate': results[0].get('plate'), 'confidence': results[0].get('confidence')})
    return render(request, 'check.html', context)

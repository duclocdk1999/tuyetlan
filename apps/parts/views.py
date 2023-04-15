import json

from apps.parts.models import MotorbikePart
from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.views import View

# Create your views here.

class PartView(View):
    def get(self, request):
        parts = MotorbikePart.objects.all()
        data = serializers.serialize('json', parts)
        return HttpResponse(data)
        
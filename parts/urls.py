from .views import retrieveMotorbikeParts
from django.urls import path

urlpatterns = [
    path('', view=retrieveMotorbikeParts, name='retrieve_motorbike_parts')
]

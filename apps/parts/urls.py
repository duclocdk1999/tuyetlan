from apps.parts.schema import schema
from apps.parts.views import PartView

from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('list', view=PartView.as_view(), name='parts_restapi'),
    path('', GraphQLView.as_view(graphiql=True, schema=schema))
]

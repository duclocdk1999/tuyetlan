import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from apps.parts.models import MotorbikePart
from custom.relay import CustomNode

class PartNode(DjangoObjectType):
    class Meta:
        model           = MotorbikePart
        filter_fields   = {
            "id":               ['exact'], 
            "barcode":          ['exact', 'icontains', 'istartswith'],
            "name_vn":          ['exact', 'icontains', 'istartswith'], 
            "name_en":          ['exact', 'icontains', 'istartswith'],
            "category__name_vn":['exact', 'icontains', 'istartswith'],
            "category__name_en":['exact', 'icontains', 'istartswith'],
            "company__name_vn": ['exact', 'icontains', 'istartswith'],
            "company__name_en": ['exact', 'icontains', 'istartswith']
        }
        interfaces      = [CustomNode]


class Query(graphene.ObjectType):
    parts   = DjangoFilterConnectionField(PartNode)

    
    @login_required
    def resolve_parts(self, info, **args):
        queryset = MotorbikePart.objects.all()
        return queryset


schema = graphene.Schema(query=Query)
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from apps.parts.models import MotorbikePart


class PartNode(DjangoObjectType):
    class Meta:
        model           = MotorbikePart
        filter_fields   = ["name_vn", "name_en", "category", "id"]
        interfaces      = [relay.Node]


class Query(graphene.ObjectType):
    part        = relay.Node.Field(PartNode)
    all_parts   = DjangoFilterConnectionField(PartNode)


schema = graphene.Schema(query=Query)
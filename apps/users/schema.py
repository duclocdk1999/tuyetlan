import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from apps.users.models import CustomUser


class CustomUserType(DjangoObjectType):
    class Meta:
        model   = CustomUser
        fields  = ["name", "email", "username"]


class Query(graphene.ObjectType):
    all_users = graphene.List(CustomUserType)

    @login_required
    def resolve_all_users(self, info):
        queryset = CustomUser.objects.all()
        return queryset
    

class Mutation(graphene.ObjectType):
    token_auth      = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token    = graphql_jwt.Verify.Field()
    refresh_token   = graphql_jwt.Refresh.Field()

    
schema = graphene.Schema(query=Query, mutation=Mutation)
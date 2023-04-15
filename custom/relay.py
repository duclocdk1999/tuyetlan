import base64
from graphene.relay import Node
from graphql_relay import from_global_id, to_global_id

class CustomNode(Node):
    class Meta:
        name = "Node"

    @staticmethod
    def to_global_id(type_, id):
        return id

from graphene.relay import Node

class CustomNode(Node):
    class Meta:
        name = "Node"

    @staticmethod
    def to_global_id(type, id):
        return id

import json

class CompositeElementEncoder(json.JSONEncoder):
    def default(self, obj):
        return {
            'chunk': str(obj)
        }
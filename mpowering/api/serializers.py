# mpowering/api/serializers.py
import json

from tastypie.serializers import Serializer

class PrettyJSONSerializer(Serializer):
    json_indent = 4

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)
        
        
class ResourceSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        
        if 'objects' in data:
            for o in data['objects']:
                self.format_resource(o)
        else:
            self.format_resource(data)
            
        return json.dumps(data,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

    def format_resource(self, data):
        # refactor tags
        
        for tag in data['tags']:
            del tag['id']
            del tag['create_date']
            for qkey, qvalue in tag['tag'].items():
                if qvalue is not None:
                    tag[qkey] = qvalue
            del tag['tag']
            
        # refactor organisations
        for org in data['organisations']:
            del org['id']
            del org['create_date']
            for qkey, qvalue in org['organisation'].items():
                if qvalue is not None:
                    org[qkey] = qvalue
            del org['organisation']
        return data  
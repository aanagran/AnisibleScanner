from rest_framework import serializers
from cis.models import HostConfig

class HostConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostConfig
        fields = ('id','ip_address','username','password','os_type','status',
                  'created_on','created_by')
        extra_kwargs={
            'id':{'read_only': True},
            'ip_address':{'required':True,'allow_null':False,'allow_blank':False},
            'username':{'required':True,'allow_null':False,'allow_blank':False},
            'password':{'required':True,'allow_null':False,'allow_blank':False},
            'status':{'read_only': True,'allow_null':False,'allow_blank':False},
            'created_on':{'read_only': True},
            'created_by':{'required':True},
        }
    
    def to_representation(self, instance):
        formate = '%Y-%m-%d %H:%M:%S'
        response =  super().to_representation(instance)
        response['created_by']=instance.created_by.first_name
        response['os_type'] = instance.get_os_type_display()
        response['created_on'] = instance.created_on.strftime(formate)
        return response
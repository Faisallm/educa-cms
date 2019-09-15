from rest_framework import serializers
from ..models import Subject, Course, Module, Content


# output data need to be serialized then rendered in a particular format
# input data need to be parsed then de-serialized for processing
# the serialized data need to be rendered in a specific format(json, xml) before it is returned in 
# http response
# the input data need to be parsed then de-serialized before we can operate on i

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order','title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    # nesting the module serializer in the  course serializer
    modules = ModuleSerializer(many=True, read_only=True)
    # many=True(to indicate that we are serializing multiple objects)
    # read_only=True(this field in read-only and should not be included in any input
    # so as to create or update objects)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order', 'item']

class ModuleWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order','title', 'description', 'contents']

class CourseWithContentSerializer(serializers.ModelSerializer):
    """CourseWithContentSerializer is now a triple nested serializer.
    showing details for course, modules and contents"""
    modules = ModuleWithContentSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']

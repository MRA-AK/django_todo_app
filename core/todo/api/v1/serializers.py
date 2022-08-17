from rest_framework.serializers import ModelSerializer

from todo.models import Task


class TaskSerializer(ModelSerializer):
    """
    A serializer for Task model
    """
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'completed']
        # fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep["created_at"] = instance.created_date
            rep["updated_at"] = instance.updated_date
        rep['priority'] = instance.get_priority_display()
        if rep['completed']:
            rep['completed'] = 'Yes'
        else:
            rep['completed'] = 'No'

        return rep

from rest_framework import serializers
from inventory.models import User, Items


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class ItemsSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        if obj.added_by_id:
            user = User.objects.get(id=obj.added_by_id)
            return UserSerializer(user).data

    class Meta:
        model = Items
        fields = "__all__"

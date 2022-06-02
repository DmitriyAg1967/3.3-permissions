
from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer( read_only=True,)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data, id__lt=None):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context["request"].user
        if self.context["request"].method!='PATCH':
            if Advertisement.objects.filter(creator_id=user.id):
                if Advertisement.objects.filter(creator_id=user.id).filter(status='OPEN').count()>3:
                    raise ValidationError('Запрещено иметь более 10 открытых объявлений')

        return data

from rest_framework import serializers
from .models import Article
from taggit.serializers import TaggitSerializer, TagListSerializerField


class ArticleSerializer(TaggitSerializer,
                        serializers.ModelSerializer):
    tagList = TagListSerializerField()

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description',
                  'body', 'tagList', 'createdAt',
                  'updatedAt', 'author']

    def is_M2M(self, instance, user_pk):

        return instance.filter(pk=user_pk).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {
            'username': instance.author.username,
            'bio': instance.author.bio,
            'image': f'{instance.author.image}',
            'subscribed': self.is_M2M(instance.author.subscriptions, self.context['request'].user.pk)
        }
        return representation



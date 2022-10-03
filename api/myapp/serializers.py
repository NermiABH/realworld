from rest_framework import serializers
from .models import Article
from taggit.serializers import TaggitSerializer, TagListSerializerField


class ArticleSerializer(TaggitSerializer,
                        serializers.ModelSerializer):
    tagList = TagListSerializerField()
    favorited = serializers.ReadOnlyField(default=False)

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'tagList', 'createdAt',
                  'updatedAt', 'favorited', 'favoritesCount',
                  'likes', 'dislikes', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {
            'username': instance.author.username,
            'bio': instance.author.bio,
            'image': f'{instance.author.image}',
        }
        if self.context['request'].user.is_authenticated:
            representation['favorited'] = self.context['request'].user.favourites.filter(
                                            pk=instance.pk
                                        ).exists()
            representation['author']['following'] = self.context['request'].user.subscriptions.filter(
                                                        pk=instance.author.pk
                                                    ).exists()
        else:
            representation['author']['following'] = False

        return representation


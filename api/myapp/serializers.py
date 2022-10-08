from rest_framework import serializers
from .models import Article, Comment
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField


class ArticleSerializer(TaggitSerializer,
                        serializers.ModelSerializer):
    tagList = TagListSerializerField(default=[])
    favorited = serializers.ReadOnlyField(default=False)

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'tagList', 'createdAt',
                  'updatedAt', 'favorited', 'favoritesCount',
                  'likes', 'dislikes', 'author')
        read_only_fields = ('author', )

    def to_representation(self, instance):
        if self.context['request'].method =='GET':
            representation = super().to_representation(instance)
            representation['author'] = {
                'username': instance.author.username,
                'bio': instance.author.bio,
                'image': f'{instance.author.image}',
            }
            if self.context['request'].user.is_authenticated:
                representation['favorited'] = self.context['request'].user.favourites.filter(
                    pk=instance.pk).exists()
                representation['author']['sent_requests'] = self.context['request'].user.sent_requests.filter(
                    pk=instance.author.pk).exists()
            else:
                representation['author']['following'] = False

            return representation
        elif self.context['request'].method=='POST':
            representation = {
                'title': instance.title,
                'description': instance.description,
                'body': instance.body,
                'tagList': instance.tagList.names(),
            }
            return representation
        elif self.context['request'].method=='PUT' or self.context['request'].method=='PATCH':
            representation = self.context['request'].data
            return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'article', 'createdAt', 'updatedAt', 'changed', 'body', 'author')
        read_only_fields = ('article', 'changed', 'author')

    def to_representation(self, instance):
        if self.context['request'].method =='GET':
            representation = super().to_representation(instance)
            representation['author'] = {
                'username': instance.author.username,
                'bio': instance.author.bio,
                'image': f'{instance.author.image}',
            }
            if self.context['request'].user.is_authenticated:
                representation['author']['sent_request'] = self.context['request'].user.sent_requests.filter(
                    pk=instance.author.pk
                ).exists()
            else:
                representation['author']['sent_request'] = False
        else:
            representation = {
                'body': instance.body
            }
        return representation
from rest_framework import serializers
from .models import Article, Comment, CustomUser
from taggit.serializers import TaggitSerializer, TagListSerializerField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'name', 'surname',
                  'bio', 'image', 'date_of_joining',
                  'date_of_birth', 'followers', 'sent_requests',
                  'favorites')
        read_only_fields = ('followers',)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        i=0
        for favorite_id in representation['favorites']:
            favorite = instance.favorites.get(pk=favorite_id)
            representation['favorites'][i]= {
                'title': favorite.title,
                'description': favorite.description,
                'body': favorite.body,
                'author': favorite.author.username}
            i+=1
        i=0
        for followers_id in representation['followers']:
            follower = instance.followers.get(pk=followers_id)
            representation['followers'][i]={
                'username': follower.username,
                'image': f'{follower.image}'}
            i+=1
        if 'username' in self.context['kwargs']:
            representation.pop('sent_requests')
        else:
            i = 0
            for sent_request_id in representation['sent_requests']:
                sent_request = instance.followers.get(pk=sent_request_id)
                representation['sent_requests'][i] = {
                    'username': sent_request.username,
                    'image': f'{sent_request.image}'}
                i += 1
        return representation

class ArticleSerializer(TaggitSerializer,
                        serializers.ModelSerializer):
    tagList = TagListSerializerField(default=[])
    favorited = serializers.ReadOnlyField(default=False)
    liked = serializers.ReadOnlyField(default=False)
    disliked = serializers.ReadOnlyField(default=False)

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'tagList', 'createdAt',
                  'updatedAt', 'favorited', 'liked',
                  'disliked', 'favoritesCount', 'likesCount',
                  'dislikesCount', 'author')
        read_only_fields = ('author', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {
            'username': instance.author.username,
            'bio': instance.author.bio,
            'image': f'{instance.author.image}',
        }
        if self.context['request'].user.is_authenticated:
            representation['favorited'] = self.context['request'].user.favorites.filter(
                pk=instance.pk).exists()
            representation['liked'] = self.context['request'].user.liked_articles.filter(
                pk=instance.pk).exists()
            representation['disliked'] = self.context['request'].user.disliked_articles.filter(
                pk=instance.pk).exists()
            representation['author']['following'] = self.context['request'].user.sent_requests.filter(
                pk=instance.author.pk).exists()
        else:

            representation['author']['following'] = False
        return representation


class CommentSerializer(serializers.ModelSerializer):
    liked = serializers.ReadOnlyField(default=False)
    disliked = serializers.ReadOnlyField(default=False)
    class Meta:
        model = Comment
        fields = ('id', 'article', 'body', 'createdAt', 'updatedAt',
                  'liked', 'disliked', 'likesCount', 'dislikesCount', 'changed', 'author')
        read_only_fields = ('article', 'changed', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {
            'username': instance.author.username,
            'bio': instance.author.bio,
            'image': f'{instance.author.image}',
        }
        if self.context['request'].user.is_authenticated:
            representation['liked'] = self.context['request'].user.liked_comments.filter(
                pk=instance.pk).exists()
            representation['disliked'] = self.context['request'].user.disliked_comments.filter(
                pk=instance.pk).exists()
            representation['author']['sent_request'] = self.context['request'].user.sent_requests.filter(
                pk=instance.author.pk
            ).exists()
        else:
            representation['author']['sent_request'] = False

        return representation
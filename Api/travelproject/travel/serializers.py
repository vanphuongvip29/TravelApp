
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class UserSerializer(ModelSerializer):

    avatar = SerializerMethodField()

    def get_avatar(self, avatar):

        name = avatar.avatar.name
        if name.startswith("static/"):
            path = 'http://127.0.0.1:8000/%s' % name

        else:
            path = 'http://127.0.0.1:8000/static/%s' % name

        return path

    # def get_avatar(self, user):
    #     request = self.context['request']
    #     if user.avatar:
    #         name = user.avatar.name
    #         if name.startswith("static/"):
    #             path = '/%s' % name
    #         else:
    #             path = '/static/%s' % name
    #
    #         return request.build_absolute_uri(path)





    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar"]
        extra_kwargs = {
            'password': {'write_only': 'True'}
        }
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user



class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class TourSerializer(ModelSerializer):
    tag = TagSerializer(many=True)

    image = SerializerMethodField()




    def get_image(self, tour):
        request = self.context['request']
        name = tour.image.name
        if name.startswith("static/"):
            path = '/%s' % name

        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Tour
        fields = ["id", "name", "image", "location", "tag", "rate","start_date","end_date","price_for_adults","price_for_children"]

class ImageTourSerializer(ModelSerializer):

    image = SerializerMethodField()



    def get_image(self, imagetour):

        name = imagetour.image.name
        if name.startswith("static/"):
            path = 'http://127.0.0.1:8000/%s' % name

        else:
            path = 'http://127.0.0.1:8000/static/%s' % name


        return path


    class Meta:
        model = ImageTour
        fields = ["id", "image", "descriptions", "tour"]

class CommentSerializer(ModelSerializer):
    user = SerializerMethodField()

    def get_user(self, comment):
        return UserSerializer(comment.user, context={"request": self.context.get('request')}).data

    class Meta:
        model = Comment
        fields = ["id", "content", "created_date", "updated_date","user"]

class GetCommentSerializer(ModelSerializer):
    user = UserSerializer()


    class Meta:
        # ordering: ['id']
        exclude = ['tour']
        model = Comment

class BookTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        exclude = []

class CreateBookTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        fields = ["num_of_adults", "num_of_children", "user", "tour"]

class BillSerializer(ModelSerializer):

    class Meta:
        model = Bill
        exclude = []


class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]

class RateSerializer(ModelSerializer):

    class Meta:
        model = Rate
        fields = ["id", "star_rate", "created_date"]

class TourViewSerializer(ModelSerializer):

    class Meta:
        model = TourView
        fields = ["id", "views", "tour"]
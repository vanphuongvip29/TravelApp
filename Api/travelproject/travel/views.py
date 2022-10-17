from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions, generics, status, pagination
from rest_framework.views import APIView
from django.conf import settings
from .models import Tour
from .serializers import *
from rest_framework.parsers import MultiPartParser
from .paginator import BasePagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from .paginator import *


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView,
                  generics.DestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='get_bill_paid', detail=False)
    def get_bill_paid(self, request):
        user = request.user
        if user:
            bill_paid = Bill.objects.filter(book_tour__user=user, active = True)

            return Response(BillSerializer(bill_paid, many=True).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO,
                        status=status.HTTP_200_OK)


class TourViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.DestroyAPIView):
    # queryset = Tour.objects.filter(active=True)
    pagination_class = BasePagination
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'take_action', 'rate']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_queryset(self):
        tours = Tour.objects.filter(active=True)

        kw = self.request.query_params.get('kw')
        if kw is not None:
            tours = tours.filter(name__icontains=kw)

        return tours

    @action(methods=['get'], detail=True, url_path='imageTour')
    def get_imagetour(self, request, pk):
        # cách 1
        tour = Tour.objects.get(pk=pk)
        imagetour = tour.imagetour.filter(active=True)

        # cách 2
        # imagetour = self.get_object().imagetour.filter(active=True)

        return Response(ImageTourSerializer(imagetour, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="comments")
    def get_comments(self, request, pk):

        tours = Tour.objects.get(pk=pk)
        comment = tours.comment
        return Response(GetCommentSerializer(comment, many=True).data,
                        status=status.HTTP_200_OK)





    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content,
                                       tour=self.get_object(),
                                       user=request.user)

            return Response(CommentSerializer(c, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='like')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])

        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type=action_type,
                                           user=request.user,
                                           tour=self.get_object())

            return Response(ActionSerializer(action).data,
                            status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_rate')
    def get_rate(self,requet,pk):
        tours = Tour.objects.get(pk=pk)
        rate = tours.rate
        return Response(RateSerializer(rate, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])

        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rate.objects.update_or_create(
                                    # star_rate=rating,
                                    user=request.user,
                                    tour=self.get_object(),
                                    defaults={"star_rate": rating})

            return Response(RateSerializer(r).data,
                            status=status.HTTP_200_OK)



    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = TourView.objects.get_or_create(tour=self.get_object())
        v.views = F('views') + 1
        v.save()

        # v.views = int(v.views)
        v.refresh_from_db()

        return Response(TourViewSerializer(v).data,
                        status=status.HTTP_200_OK)


class ImageTourViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = ImageTour.objects.all()
    serializer_class = ImageTourSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ViewSet,
                     generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class BookTourViewSet(viewsets.ModelViewSet):

    queryset = BookTour.objects.all()
    serializer_class = CreateBookTourSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    def create(self, request):
        user = request.user
        tour = Tour.objects.get(pk = request.data.get('tour'))

        if user:
                num_of_children = request.data.get('num_of_children')
                num_of_adults = request.data.get('num_of_adults')
                try:
                    book_tour = BookTour.objects.create(num_of_adults = num_of_adults, num_of_children = num_of_children,
                                                        user = user, tour = tour)
                    serializers = BookTourSerializer(book_tour)
                    bill = Bill.objects.create(book_tour = book_tour)
                    total_price = tour.price_for_children * float(num_of_children) + float(num_of_adults) * tour.price_for_adults
                    bill.total_price = total_price
                    bill.save()
                    return Response(data=serializers.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    err_msg = e.__str__()
        return Response(data={
                    'error_msg': err_msg
                },status=status.HTTP_400_BAD_REQUEST)


class BillViewSet(viewsets.ViewSet,generics.RetrieveAPIView,
                  generics.UpdateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = BillSerializer
    queryset = Bill.objects.filter(active = True)

    @action(methods=['post'], url_path='thanh_toan', detail=True)
    def thanh_toan(self, request, pk):
        bill = self.get_object()
        if bill:
            if bill.active == True:
                bill.active = False

                bill.save()

                return Response(data={"message": "Payment successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Bill paid"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


def index(request):
    return HttpResponse("tour app")

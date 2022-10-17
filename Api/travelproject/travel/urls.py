
from django.urls import path, include
from .admin import admin_site
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register('tours', views.TourViewSet,basename='tour')
routers.register('users', views.UserViewSet)
routers.register('tags', views.TagViewSet)
routers.register('imagetours', views.ImageTourViewSet, basename='imagetour')
routers.register('comments', views.CommentViewSet, basename='comment')
routers.register('booktours', views.BookTourViewSet, basename='booktour')
routers.register('bills', views.BillViewSet, basename='bill')

urlpatterns = [

    path('', include(routers.urls)),
    path('oauth2-info/',views.AuthInfo.as_view()),
    path('admin/', admin_site.urls),
]


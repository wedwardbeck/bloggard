from django.urls import path

from . import views
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('', views.PostViewSet, base_name='posts')


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]
#
# urlpatterns += router.urls

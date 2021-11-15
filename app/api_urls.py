from django.urls import path, include
from rest_framework import routers
from app.views import UserViewSet, ItemViewSet, SliderViewSet, ItemFilterListView

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('item', ItemViewSet)
router.register('slider', SliderViewSet)

app_name = 'home'

urlpatterns = [
    path('', include(router.urls)),
    path('items/', ItemFilterListView.as_view(), name='items'),
]
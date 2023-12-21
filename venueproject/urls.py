from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from venueapi.views import register_user, login_user, BandViewSet, VenueViewSet, ConcertViewSet, OpenerViewSet, FavoriteViewSet 

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bands', BandViewSet, 'band')
router.register(r'venues', VenueViewSet, 'venue')
router.register(r'concerts', ConcertViewSet, 'concert')
router.register(r'openers', OpenerViewSet, 'opener')
router.register(r'favorites', FavoriteViewSet, 'favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls)
]
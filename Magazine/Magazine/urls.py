from django.contrib import admin
from django.db import router
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest.views import *

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'cats', CatViewSet)
router.register(r'comment', CommViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/comment/post/<int:post>/', CommViewSet.as_view({'get': 'list'})),
    # path('api/v1/comment/', CommViewSet.as_view({'post': 'create'})),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

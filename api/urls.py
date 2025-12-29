from django.urls import path, include # type: ignore
from rest_framework.routers import SimpleRouter # type: ignore
from api.views import PostagemViewSet, FollowViewSet 

router = SimpleRouter()
router.register(r'postagens', PostagemViewSet, basename='postagem')
router.register(r'follows', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
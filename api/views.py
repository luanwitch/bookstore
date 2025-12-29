from rest_framework import viewsets, mixins, status # type: ignore
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework import serializers # type: ignore

from django.contrib.auth import get_user_model # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore

from .models import Postagem, Follow
from .serializers import PostagemSerializer, FollowSerializer

User = get_user_model()


# =========================================================================
# 1. VIEWSET DE POSTAGENS (O FEED DO TWITTER)
# =========================================================================

class PostagemViewSet(viewsets.ModelViewSet):
    serializer_class = PostagemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Usuário não autenticado → vê tudo
        if not self.request.user.is_authenticated:
            return Postagem.objects.all().order_by('-data_criacao')

        # Obtém IDs dos usuários seguidos
        followed_users_ids = self.request.user.seguidos_set.values_list(
            'followed_id', flat=True
        ).distinct()

        # Concatena com o próprio usuário
        feed_authors_ids = list(followed_users_ids)
        feed_authors_ids.append(self.request.user.id)

        return Postagem.objects.filter(
            autor__in=feed_authors_ids
        ).order_by('-data_criacao')

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


# =========================================================================
# 2. VIEWSET DE FOLLOW (SEGUIR / DEIXAR DE SEGUIR)
# =========================================================================

class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['followed']

        # Previne seguir a si mesmo
        if self.request.user == followed_user:
            raise serializers.ValidationError(
                {"followed": "Você não pode seguir a si mesmo."}
            )

        serializer.save(follower=self.request.user)

    def destroy(self, request, *args, **kwargs):
        followed_id = kwargs.get('pk')

        try:
            instance = Follow.objects.get(
                follower=request.user,
                followed_id=followed_id
            )
        except Follow.DoesNotExist:
            return Response(
                {"detail": "Relacionamento de seguimento não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def seguidores(self, request):
        seguidores = Follow.objects.filter(followed=request.user)
        serializer = self.get_serializer(seguidores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def seguidos(self, request):
        seguidos = self.get_queryset()
        serializer = self.get_serializer(seguidos, many=True)
        return Response(serializer.data)

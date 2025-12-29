from rest_framework import serializers # type: ignore
from .models import Postagem, Follow 

class PostagemSerializer(serializers.ModelSerializer):
   
    autor_username = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = Postagem
        fields = ['id', 'autor', 'autor_username', 'conteudo', 'data_criacao']
    
        read_only_fields = ['autor', 'autor_username', 'data_criacao']

    def validate_conteudo(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("O conteúdo da postagem não pode ser vazio.")
        return value
    


class FollowSerializer(serializers.ModelSerializer):
 
    follower_username = serializers.ReadOnlyField(source='follower.username')
    followed_username = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follow
        
        fields = ['id', 'follower', 'follower_username', 'followed', 'followed_username', 'data_criacao']
        read_only_fields = ['follower', 'follower_username', 'followed_username', 'data_criacao']    
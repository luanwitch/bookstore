from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Postagem(models.Model):
    """
    Representa uma postagem (Tweet) na rede social.
    """
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='postagens' 
    )
    
    conteudo = models.TextField(
        max_length=280, 
        blank=False,
        null=False
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-data_criacao'] 
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'

    def __str__(self):
        
        return f'{self.autor.username}: {self.conteudo[:30]}...'

class Follow(models.Model):
    """
    Registra um relacionamento de 'seguidor' (follower) e 'seguido' (followed).
    """
    follower = models.ForeignKey(
        User, 
        related_name='seguidores_set',
        on_delete=models.CASCADE
    )

    followed = models.ForeignKey(
        User, 
        related_name='seguidos_set',
        on_delete=models.CASCADE
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed',)
        verbose_name = 'Seguimento'
        verbose_name_plural = 'Seguimentos'

    def __str__(self):
        return f'{self.follower.username} segue {self.followed.username}'    

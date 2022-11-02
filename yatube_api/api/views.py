from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from posts.models import Post, User, Group, Comment, Follow
from .serializers import GroupSerializer, PostSerializer
from .serializers import UserSerializer, CommentSerializer, FollowSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Получение списка всех постов (GET запрос к api/v1/posts).
    При указании параметров limit и offset выдача работает с пагинацией.
    Создание нового поста (POST запрос к api/v1/posts).
    Получение, редакция и удаление поста по id
    (GET, PUT, PATH, DELETE запросы к api/v1/posts/post_id).
    Анонимные запросы запрещены. Изменение чужого контента запрещено.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Автор создаваемого поста - пользователь."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка всех групп (GET запрос к api/v1/groups).
    Получение информации о группе по id
    (GET к api/v1/groups/group_id).
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Пользователь."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """api/v1/posts/{post_id}/comments/ (GET, POST).
    Получаем список всех комментариев поста с id=post_id или создаём новый.
    api/v1/posts/{post_id}/comments/{comment_id}/ (GET, PUT, PATCH, DELETE):
    получаем, редактируем или удаляем комментарий по id у поста с id=post_id.
    POST запросы только для авторизованных пользователей,
    изменение чужого контента запрещено.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Выбор всех комментариев к конкретному посту."""
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        new_queryset = Comment.objects.filter(post=post)

        return new_queryset

    def perform_create(self, serializer):
        """Автор создаваемого комментария - пользователь.
        Пост - пост с id = post_id."""
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Эндпоинт api/v1/follow/ и два метода: GET и POST.
    GET — возвращает все подписки пользователя, сделавшего запрос.
    Возможен поиск по подпискам по параметру search.
    POST — подписать пользователя, сделавшего запрос на пользователя,
    переданного в теле запроса. При попытке подписаться на самого себя,
    пользователь получит информативное сообщение об ошибке.
    Анонимный пользователь на запросы к этому эндпоинту получает
    ответ с кодом 401 Unauthorized.
    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Выбор всех подписок пользователя, сделавшего запрос."""
        new_queryset = Follow.objects.filter(user=self.request.user)

        return new_queryset

    def perform_create(self, serializer):
        """Создание новой подписки."""

        serializer.save(
            user=self.request.user,
            following=get_object_or_404(
                User, username=self.request.data['following']
            )
        )

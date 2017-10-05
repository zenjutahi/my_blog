from django.db.models import Q

from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,


	)

from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from rest_framework import generics


from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,

	)

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination


from comments.models import Comment 

from .serializers import ( 
	CommentListSerializer,
	CommentDetailSerializer,
	create_comment_serializer,
	)


class CommentCreateAPIView(generics.CreateAPIView):
	queryset = Comment.objects.all()
	#permission_classes = [IsAuthenticated]
	def get_serializer_class(self):
		model_type = self.request.GET.get("type")
		slug = self.request.GET.get("slug")
		parent_id = self.request.GET.get("parent_id", None)
		return create_comment_serializer(
				model_type='post', 
				slug=slug, 
				parent_id=parent_id,
				user=self.request.user,
				)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destory(request, *args, **kwargs)

#class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
#	queryset = Post.objects.all()
#	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#	def perform_update(self, serializer):
#         
#class PostDeleteAPIView(generics.DestroyAPIView):
#	queryset = Post.objects.all()
#	serializer_class = PostDetailSerializer
#	lookup_field = 'slug'
#	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentListAPIView(generics.ListCreateAPIView):
	serializer_class = CommentListSerializer
	permission_classes = [IsOwnerOrReadOnly]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['content', 'user__first_name']
	pagination_class = PostPageNumberPagination


	def get_queryset(self, *args, **kwargs):
		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Comment.objects.all().filter(id__gte=0)
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list



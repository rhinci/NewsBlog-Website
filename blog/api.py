from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer, UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#@method_decorator(csrf_exempt, name='dispatch')
class ArticleApi(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['created_date', 'title']

    def get_queryset(self):
        queryset = Article.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        categories = self.request.query_params.get('categories')
        if categories:
            category_list = categories.split(',')
            q_objects = Q()
            for cat in category_list:
                q_objects |= Q(category=cat)
            queryset = queryset.filter(q_objects)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='category/(?P<category>[^/.]+)')
    def filter_by_category(self, request, category=None):
        articles = Article.objects.filter(category=category)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sort/(?P<field>[^/.]+)')
    def sort_articles(self, request, field=None):
        if field == 'date':
            articles = Article.objects.all().order_by('created_date')
        elif field == 'date_desc':
            articles = Article.objects.all().order_by('-created_date')
        else:
            articles = Article.objects.all()
        
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


class CommentApi(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    
    def perform_create(self, serializer):
        serializer.save()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Пользователь успешно создан"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, decorators, response, status
from rest_framework.permissions import AllowAny
from apps.jobs.models import JobApplication
from .serializers import JobApplicationSerializer
from django.http import JsonResponse
class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class=JobApplicationSerializer
    def get_queryset(self): return JobApplication.objects.filter(user=self.request.user)
    def perform_create(self,serializer): serializer.save(user=self.request.user)
    @decorators.action(detail=False,methods=['get'])
    def dashboard(self,request):
        qs=self.get_queryset()
        return response.Response({'total':qs.count(),'by_status':{x['status']:x['count'] for x in qs.values('status').annotate(count=Count('id'))},'upcoming':JobApplicationSerializer(qs.filter(next_action_date__isnull=False).order_by('next_action_date')[:5],many=True).data})
@decorators.api_view(['get'])
def health(request): return JsonResponse({'status':'ok','service':'job-tracker-api'})
@decorators.api_view(['post'])
@decorators.permission_classes([AllowAny])
def register(request):
    username=request.data.get('username'); password=request.data.get('password'); email=request.data.get('email','')
    if not username or not password: return response.Response({'detail':'username and password are required'},status=400)
    if User.objects.filter(username=username).exists(): return response.Response({'detail':'username already exists'},status=400)
    user=User.objects.create_user(username=username,password=password,email=email)
    return response.Response({'id':user.id,'username':user.username},status=status.HTTP_201_CREATED)
# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Proposal, Notification
from .serializers import ProposalSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        proposal.receiver = request.user
        proposal.save()
        Notification.objects.create(user=proposal.sender, message=f'{request.user.username}님이 제의를 수락했습니다.')
        return Response({'message': 'Proposal accepted.'})

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # 요청 데이터에서 필요한 정보 추출
        message = request.data.get('message')
        
        # 필수 필드가 있는지 확인
        if not message:
            return Response({"error": "Message field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 현재 로그인한 사용자를 가져오거나, 필요한 경우 request.user.id를 사용하여 사용자 ID를 설정
            user = request.user
        except AttributeError:
            return Response({"error": "User authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Notification 객체 생성
        notification = Notification.objects.create(user=user, message=message)
        
        # 생성된 Notification 객체를 시리얼라이즈하여 응답
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
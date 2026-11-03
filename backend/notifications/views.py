from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """GET -> the logged-in user's 50 most recent notifications."""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)[:50]


class UnreadCountView(APIView):
    """GET -> how many unread notifications the logged-in user has."""

    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})


class MarkReadView(APIView):
    """POST -> mark one of the logged-in user's notifications as read."""

    def post(self, request, pk):
        updated = Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
        if not updated:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Marked as read.'})


class MarkAllReadView(APIView):
    """POST -> mark all of the logged-in user's notifications as read."""

    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})
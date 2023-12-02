from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import generics
from .models import ChatRoom, Message, CustomUser
from .serializers import ChatRoomSerializer, MessageSerializer, UserSerializer , JoinChatRoomSerializer
from rest_framework import permissions, viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows creation of chatroom
    """
    queryset = ChatRoom.objects.all().order_by('-id')
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        user = self.request.user

        user_chatrooms = ChatRoom.objects.filter(members=user)

        queryset = Message.objects.filter(chatroom__in=user_chatrooms).order_by('-id')

        return queryset
    
    def perform_create(self, serializer):
        chatroom = serializer.validated_data['chatroom']

        if self.request.user not in chatroom.members.all():
            raise ValidationError("You are not a member of this chatroom.")

        serializer.save(user=self.request.user)
            

class JoinChatRoom(generics.UpdateAPIView):
    """
    API endpoint that allows joining a chat room
    """
    queryset = ChatRoom.objects.all()
    serializer_class = JoinChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, pk=None):
        serializer = JoinChatRoomSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            chatroom = ChatRoom.objects.get(id=pk)
            user_to_be_removed = serializer.data['members'][0]
            chatroom.members.add(user_to_be_removed)
            chatroom.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LeaveChatRoom(generics.UpdateAPIView):
    """
    API endpoint that allows leaving a chat room
    """
    queryset = ChatRoom.objects.all()
    serializer_class = JoinChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, pk=None):
        serializer = JoinChatRoomSerializer(data=request.data)
        
        if serializer.is_valid():
            chatroom = ChatRoom.objects.get(id=pk)
            user_to_be_removed = serializer.data['members'][0]
            chatroom.members.remove(user_to_be_removed)
            chatroom.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from chat import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), #swagger
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), #swagger
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), #swagger
    path('joinchatroom/<pk>/', views.JoinChatRoom.as_view()),
    path('leavechatroom/<pk>/', views.LeaveChatRoom.as_view()),
    
    
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        
#API
router.register(r'users', views.UserViewSet)
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'chatrooms', views.ChatRoomViewSet)

urlpatterns += [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
         ]

urlpatterns += router.urls
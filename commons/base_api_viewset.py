from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# base api viewset for all api viewsets
class BaseApiViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset()
    
    def error_response(self, message):
        return Response({
            'message': message,
            'status_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def success_response(self, message, data=None):
        return Response({
            'message': message,
            'data': data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

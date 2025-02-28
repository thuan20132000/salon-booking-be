from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# base api viewset for all api viewsets
class BaseApiViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.success_response('Retrieved successfully', response.data)
        except Exception as e:
            return self.error_response(str(e))
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return self.success_response('Created successfully', response.data)
        except Exception as e:
            return self.error_response(str(e))
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.success_response('Updated successfully', response.data, status.HTTP_200_OK)
        except Exception as e:
            return self.error_response(str(e))
    
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return self.success_response('Deleted successfully', response.data, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self.error_response(str(e))
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset()
    
    def error_response(self, message):
        return Response({
            'message': message,
            'status_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def success_response(self, message, data=None, status_code=status.HTTP_200_OK):
        return Response({
            'message': message,
            'data': data,
            'status_code': status_code
        }, status=status_code)
    

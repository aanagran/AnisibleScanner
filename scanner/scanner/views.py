from rest_framework import status, views
from rest_framework.response import Response


class ProbeCheck(views.APIView):
    http_method_names = ["get"]

    def get(self,request):
        response = {'status':200,'data':'OK'}
        return Response(response, status=status.HTTP_200_OK)
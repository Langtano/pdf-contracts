from rest_framework import viewsets
from pdf_contracts.utils.util import create_response
from .serializer import GeneratePdfSerializer


class GeneratePdfViewSet(viewsets.ViewSet):

    def create(self, request):
        validate = GeneratePdfSerializer(data=request.data)
        validate.is_valid(raise_exception=True)
        try:
            result = validate.generate_contract()
            if result['success']:
                return create_response(True, 201, '', result['message'], 0)
            return create_response(False, 500, '', result['message'], 0)
        except Exception as e:
            return create_response(False, 500, {}, e, 0)

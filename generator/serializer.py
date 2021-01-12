from rest_framework import serializers
from .dao_generator import GeneratorPdfDao


class GeneratePdfSerializer(serializers.Serializer):
    contract_type = serializers.CharField()
    creditor = serializers.CharField()
    rfc = serializers.CharField()
    written_amount = serializers.CharField()
    number_amount = serializers.CharField()
    written_deadline_days = serializers.CharField()
    number_deadline_days = serializers.CharField()
    deadline_date = serializers.CharField()
    bank = serializers.CharField()
    clabe = serializers.CharField()
    beneficiary_name = serializers.CharField()
    beneficiary_email = serializers.EmailField()
    beneficiary_phone = serializers.CharField()
    beneficiary_relationship = serializers.CharField()
    creditor_phone = serializers.CharField()
    creditor_atention = serializers.CharField()
    creditor_email = serializers.CharField()

    def generate_contract(self):
        result = GeneratorPdfDao.generate_pdf(self, contract=self.data)
        return result
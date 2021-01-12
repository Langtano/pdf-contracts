from pdf_contracts.utils.util import PdfGenerator

class GeneratorPdfDao:
    def generate_pdf(self, contract):
        if contract['contract_type'] == 'dynamic':
            return PdfGenerator.generate_dynamic_contract(contract=contract)
        else:
            return PdfGenerator.generate_standard_contract(contract=contract)
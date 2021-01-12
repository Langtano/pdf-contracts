from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle, Image, Paragraph
import datetime
import math
from . import constants


def create_response(success: bool, status: int, data: object, message: object, code: int):

    status = 200
    if success:
        code = 200

    response = {
        'success': success,
        'code': code,
        'data': data,
        'message': message
    }

    return Response(response, status=status)


class Helpers:
    def __init__(self):
        pass

    @staticmethod
    def get_today_date():
        today = datetime.date.today()
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")
        month = constants.MONTH['{}'.format(month)]
        return day, month, year

    @staticmethod
    def statement_split(creditor):
        splited_statement = []
        statement = constants.STATEMENT.replace('__CREDITOR__', creditor.upper())
        while len(statement) >= constants.STATEMENT_MAX_LEN:
            if statement[0] == ' ':
                statement = statement[1:]
            if statement[constants.STATEMENT_MAX_LEN] == ' ':
                splited_statement.append(statement[0:constants.STATEMENT_MAX_LEN])
                statement = statement[constants.STATEMENT_MAX_LEN:]
            else:
                aux_statement = statement[0:constants.STATEMENT_MAX_LEN]
                space_index = aux_statement.rfind(' ')
                splited_statement.append(statement[0:space_index])
                statement = statement[space_index:]
        if statement[0] == ' ':
            statement = statement[1:]
        splited_statement.append(statement)
        return splited_statement

    @staticmethod
    def generic_clause_split(clause):
        splited_clause = []
        if len(clause) <= constants.TAB_MAX_LEN:
            splited_clause.append(clause)
            return splited_clause
        if clause[constants.TAB_MAX_LEN] == ' ':
            splited_clause.append(clause[0:constants.TAB_MAX_LEN])
            clause = clause[constants.TAB_MAX_LEN:]
        else:
            aux_statement = clause[0:constants.TAB_MAX_LEN]
            space_index = aux_statement.rfind(' ')
            splited_clause.append(clause[0:space_index])
            clause = clause[space_index:]
        while len(clause) >= constants.NO_TAB_MAX_LEN:
            if clause[0] == ' ':
                clause = clause[1:]
            if clause[constants.NO_TAB_MAX_LEN] == ' ':
                splited_clause.append(clause[0:constants.NO_TAB_MAX_LEN])
                clause = clause[constants.NO_TAB_MAX_LEN:]
            else:
                aux_statement = clause[0:constants.NO_TAB_MAX_LEN]
                space_index = aux_statement.rfind(' ')
                splited_clause.append(clause[0:space_index])
                clause = clause[space_index:]
        if clause[0] == ' ':
            clause = clause[1:]
            splited_clause.append(clause)
        return splited_clause

    @staticmethod
    def clause_3_split(clause, written_amount, number_amount):
        splited_clause_3 = []
        clause_3 = clause.replace('__WRITTEN_AMOUNT__', written_amount)
        clause_3 = clause_3.replace('__NUMBER_AMOUNT__', number_amount)
        if clause_3[constants.TAB_MAX_LEN] == ' ':
            splited_clause_3.append(clause_3[0:constants.TAB_MAX_LEN])
            clause_3 = clause_3[constants.TAB_MAX_LEN:]
        else:
            aux_statement = clause_3[0:constants.TAB_MAX_LEN]
            space_index = aux_statement.rfind(' ')
            splited_clause_3.append(clause_3[0:space_index])
            clause_3 = clause_3[space_index:]
        while len(clause_3) >= constants.NO_TAB_MAX_LEN:
            if clause_3[0] == ' ':
                clause_3 = clause_3[1:]
            if clause_3[constants.NO_TAB_MAX_LEN] == ' ':
                splited_clause_3.append(clause_3[0:constants.NO_TAB_MAX_LEN])
                clause_3 = clause_3[constants.NO_TAB_MAX_LEN:]
            else:
                aux_statement = clause_3[0:constants.NO_TAB_MAX_LEN]
                space_index = aux_statement.rfind(' ')
                splited_clause_3.append(clause_3[0:space_index])
                clause_3 = clause_3[space_index:]
        if clause_3[0] == ' ':
            clause_3 = clause_3[1:]
            splited_clause_3.append(clause_3)
        return splited_clause_3

    @staticmethod
    def standard_clause_5_split(clause, written_deadline_days, number_deadline_days, deadline_date):
        splited_clause = []
        clause = clause.replace('__WRITTEN_DEADLINE__', written_deadline_days)
        clause = clause.replace('__NUMBER_DEADLINE__', number_deadline_days)
        clause = clause.replace('__DEADLINE_DATE__', deadline_date)
        if clause[constants.TAB_MAX_LEN] == ' ':
            splited_clause.append(clause[0:constants.TAB_MAX_LEN])
            clause = clause[constants.TAB_MAX_LEN:]
        else:
            aux_statement = clause[0:constants.TAB_MAX_LEN]
            space_index = aux_statement.rfind(' ')
            splited_clause.append(clause[0:space_index])
            clause = clause[space_index:]
        while len(clause) >= constants.NO_TAB_MAX_LEN:
            if clause[0] == ' ':
                clause = clause[1:]
            if clause[constants.NO_TAB_MAX_LEN] == ' ':
                splited_clause.append(clause[0:constants.NO_TAB_MAX_LEN])
                clause = clause[constants.NO_TAB_MAX_LEN:]
            else:
                aux_statement = clause[0:constants.NO_TAB_MAX_LEN]
                space_index = aux_statement.rfind(' ')
                splited_clause.append(clause[0:space_index])
                clause = clause[space_index:]
        if clause[0] == ' ':
            clause = clause[1:]
            splited_clause.append(clause)
        return splited_clause

    @staticmethod
    def signature_header_split(day, month, year):
        splited_clause = []
        clause = constants.SIGNATURES_HEADER.replace('__DAY__', day)
        clause = clause.replace('__MONTH__', month)
        clause = clause.replace('__YEAR__', year)
        if clause[constants.TAB_MAX_LEN] == ' ':
            splited_clause.append(clause[0:constants.TAB_MAX_LEN])
            clause = clause[constants.TAB_MAX_LEN:]
        else:
            aux_statement = clause[0:constants.TAB_MAX_LEN]
            space_index = aux_statement.rfind(' ')
            splited_clause.append(clause[0:space_index])
            clause = clause[space_index:]
        while len(clause) >= constants.NO_TAB_MAX_LEN:
            if clause[0] == ' ':
                clause = clause[1:]
            if clause[constants.NO_TAB_MAX_LEN] == ' ':
                splited_clause.append(clause[0:constants.NO_TAB_MAX_LEN])
                clause = clause[constants.NO_TAB_MAX_LEN:]
            else:
                aux_statement = clause[0:constants.NO_TAB_MAX_LEN]
                space_index = aux_statement.rfind(' ')
                splited_clause.append(clause[0:space_index])
                clause = clause[space_index:]
        if clause[0] == ' ':
            clause = clause[1:]
            splited_clause.append(clause)
        return splited_clause



class PdfGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_standard_contract(contract):
        try:
            # PDF CONFIGURATIONS ------------------------------------------------------------------
            w, h = letter
            day, month, year = Helpers.get_today_date()
            contract_type = constants.CONTRACT_TYPE['{}'.format(contract['contract_type'])]
            c = canvas.Canvas('{}.pdf'.format(contract['creditor']), pagesize=letter)
            c.setTitle('Contrato {ct} {cc}'.format(ct=contract_type, cc=contract['creditor']))
            pdfmetrics.registerFont(
                TTFont('Lato', "fonts/Lato-Regular.ttf"),
            )
            pdfmetrics.registerFont(
                TTFont('Lato-Bold', "fonts/Lato-Bold.ttf"),
            )
            pdfmetrics.registerFont(
                TTFont('Montserrat', "fonts/Montserrat-Bold.ttf")
            )


            # PDF MAIN PAGE -----------------------------------------------------------------------
            c.setFont('Lato-Bold', 15)
            c.drawCentredString(x=w/2, y=(h/2)+300, text='CONTRATO DE CRÉDITO SIMPLE CON INTERÉS')
            c.drawCentredString(x=w/2, y=(h/2)+220, text='ENTRE')
            c.drawCentredString(x=w/2, y=(h/2)+140, text='{}'.format(contract['creditor'].upper()))
            c.drawCentredString(x=w/2, y=(h/2)+120, text='COMO ACREEDOR')
            c.drawCentredString(x=w/2, y=(h/2)+80, text='Y')
            c.drawCentredString(x=w/2, y=(h/2)+50, text='NAICA TECHNOLOGIES, S.A. DE C.V.')
            c.drawCentredString(x=w/2, y=(h/2)+30, text='COMO DEUDOR')
            c.drawCentredString(x=w/2, y=(h/2)-290,
                                text='{day} DE {month} DE {year}'.format(
                                day=day, month=month, year=year))
            c.showPage()


            # PDF STATEMENTS ------------------------------------------------------------------------
            statement = Helpers.statement_split(creditor=contract['creditor'])
            y_statement = 320
            for statement_line in statement:
                c.drawString(x=constants.LEFT_PADDING, y=(h/2)+y_statement, text=statement_line)
                y_statement -= 15
            new_y_statement = (h/2)+y_statement
            c.drawCentredString(x=w/2, y=new_y_statement-20, text='DECLARACIONES')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-50,
                         text='I.    Declara el Acreedor por conducto de su representante legal:')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-80,
                         text='    1.    Que es una persona física, mayor de edad, en pleno uso de sus facultades;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-110,
                         text='    2.    Que de conformidad con la regulación aplicable mantiene los requisitos necesarios')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-130,
                         text='para ser considerado un inversionista calificado;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='    3.    Que es su voluntad celebrar el presente Contrato y obligarse en los términos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='establecidos;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 210,
                         text='    4.    Que el presente Contrato constituye obligaciones legales, válidas y obligatorias del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='Acreedor, exigibles de conformidad con los términos y condiciones establecidos en el')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='presente;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 280,
                         text='    5.    Que todas las declaraciones contenidas en este Contrato son ciertas, correctas y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='verdaderas en esta fecha;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 330,
                         text='    6.    Que no existe ni tiene conocimiento de que pudiere existir o iniciarse en el futuro')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 350,
                         text='alguna acción, demanda, reclamación, requerimiento o procedimiento judicial o')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 370,
                         text='extrajudicial que afecte o pudiere afectar la legalidad, validez o exigibilidad del presente')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 390,
                         text='Contrato;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 420,
                         text='    7.    Que cuenta con Registro Federal de Contribuyentes número: {rfc}; y'.format(rfc=contract['rfc']))
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 450,
                         text='    8.    Que está dispuesta a transferir la propiedad de una suma de dinero solicitado')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 470,
                         text='por el Deudor y que cuenta con los recursos necesarios para ello, de acuerdo con los')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 490,
                         text='términos y bajo las condiciones establecidas en el presente Contrato y que dichos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 510,
                         text='recursos provienen de actividades lícitas.')
            c.drawCentredString(x=w/2, y=50, text='2')
            c.showPage()

            # PDF STATEMENTS P2 ------------------------------------------------------------------------
            new_y_statement = (h/2)+320
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement,
                         text='II.    Declara el Deudor por conducto de su representante legal:')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-30,
                         text='    1.    Que es una persona moral de nacionalidad mexicana, lo cual acredita con la')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-50,
                         text='escritura pública número 29,187 de fecha veinticinco días del mes de agosto del año dos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 70,
                         text='mil dieciséis, otorgada ante la fe del licenciado José Antonio Acosta Pérez, titular de la')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 90,
                         text='Notaría Pública número Nueve y del Patrimonio Inmobiliario Federal de la ciudad de ')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 110,
                         text='Cuernavaca, Morelos, la cual se encuentra debidamente inscrita ante el Registro Público ')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 130,
                         text='de la Propiedad y del Comercio de Cuernavaca bajo el folio mercantil número 2016024035;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='    2.    Que es su voluntad celebrar el presente Contrato y obligarse en los términos en él')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='establecidos y que conforme a su objeto social puede llevar a cabo la celebración del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 200,
                         text='presente Contrato;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='    3.    Que el presente Contrato constituye obligaciones legales, válidas y obligatorias del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='Deudor, exigibles de conformidad con los términos y condiciones establecidos en el')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 270,
                         text='presente.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='    4.    Que todas las declaraciones contenidas en este Contrato son ciertas, correctas y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 320,
                         text='verdaderas en esta fecha.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 350,
                         text='    5.    Que no existe ni tiene conocimiento de que pudiere existir o iniciarse en el futuro')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 370,
                         text='alguna acción, demanda, reclamación, requerimiento o procedimiento judicial o')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 390,
                         text='extrajudicial que afecte o pudiere afectar la legalidad, validez o exigibilidad del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 410,
                         text='presente Contrato.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 440,
                         text='    6.    Que cuenta con Registro Federal de Contribuyentes número: NTE160825PG2.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 470,
                         text='    En virtud de lo anterior, las Partes acuerdan en obligarse de conformidad con las')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 490,
                         text='siguientes:')
            c.drawCentredString(x=w/2, y=new_y_statement-520, text='C L Á U S U L A S')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-550, text='PRIMERA. DEFINICIONES .')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 570,
                         text='    Los términos con mayúscula inicial utilizados en el presente Contrato que no se')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 590,
                         text='encuentren definidos de otra manera, tendrán el significado que se atribuye a dichos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 610,
                         text='términos en la presente Cláusula y serán utilizados en forma singular o plural según')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 630,
                         text='sea aplicable.')
            c.drawCentredString(x=w / 2, y=50, text='3')
            c.showPage()

            # PDF CLAUSES & CLAUSE 2---------------------------------------------------------------------------------
            # --- TABLE START ---
            creditor_condition = ['“Acreedor”', 'Significa el señor(a) {}'.format(contract['creditor'])]
            new_y_statement = (h / 2) + 70
            clauses_table_data = constants.STANDARD_CLAUSES_DATA
            clauses_table_data.insert(0, creditor_condition)
            clauses_table_data.insert(0, constants.CLAUSES_TABLE_HEADER)
            table = Table(clauses_table_data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#000066')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 1, HexColor('#000000')),
                ('GRID', (0, 1), (-1, -1), 1, HexColor('#000000')),
                ('VALIGN', (0,0), (-1, -1), 'MIDDLE')
            ])
            table.setStyle(style)
            table._argW[0] = (w / 10) * 2
            table._argW[1] = (w / 10) * 5.5
            table.wrapOn(c, 0, 0)
            table.drawOn(c, x=constants.LEFT_PADDING, y=new_y_statement)
            # --- TABLE END ---
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 40, text='SEGUNDA. INTERPRETACIÓN INTEGRAL DEL CONTRATO.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 70,
                         text='    Las Partes acuerdan que las declaraciones, definiciones, cláusulas y anexos de este')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 90,
                         text='Contrato, son parte integrante del presente Contrato de Crédito.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 120,
                         text='    Las palabras, “del presente”, “en el presente” y “conforme al presente”, y las palabras')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 140,
                         text='de significado similar siempre que sean utilizadas en este Contrato se referirán a este')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='Contrato en su totalidad y no a disposiciones en específico del mismo. Los términos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='cláusula, declaración y anexo se refieren a las Cláusulas, Declaraciones y Anexos de')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 200,
                         text='este Contrato, salvo que se especifique lo contrario.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='    Las referencias a cualquier Persona o Personas se interpretarán como referencias a')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='cualesquiera sucesores o cesionarios de esa Persona o Personas.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 280,
                         text='    Los títulos que aparecen en cada una de las cláusulas son exclusivamente para')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='facilitar su lectura y, por consiguiente, no se considerará que definen, limitan o describen')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 320,
                         text='el contenido de las cláusulas del mismo, ni para efectos de su interpretación y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 340,
                         text='cumplimiento.')
            c.drawCentredString(x=w / 2, y=50, text='4')
            c.showPage()

            # CLAUSE 3, 4, 5 & 6 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            splited_clause_3 = Helpers.clause_3_split(clause=constants.CLAUSE_3, written_amount=contract['written_amount'], number_amount=contract['number_amount'])
            splited_clause_3_p2 = Helpers.generic_clause_split(clause=constants.CLAUSE_3_P2)
            clause_4 = Helpers.generic_clause_split(clause=constants.CLAUSE_4)
            clause_5_p1 = Helpers.standard_clause_5_split(
                clause=constants.STANDARD_CLAUSE_5_P1,
                written_deadline_days=contract['written_deadline_days'],
                number_deadline_days=contract['number_deadline_days'],
                deadline_date=contract['deadline_date']
            )
            clause_5_p2 = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_5_P2)
            clause_6_p1 = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_6_P1)
            y_aux = 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement, text='TERCERA. CRÉDITO SIMPLE.')
            for item in range(len(splited_clause_3)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement-y_aux, text=splited_clause_3[item])
                y_aux += 20

            for item in range(len(splited_clause_3_p2)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=splited_clause_3_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='CUARTA. DESTINO DE LOS FONDOS.')
            for item in range(len(clause_4)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_4[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='QUINTA. PLAZO.')
            for item in range(len(clause_5_p1)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_5_p1[item])
                y_aux += 20
            for item in range(len(clause_5_p2)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_5_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='SEXTA. INTERESES ORDINARIOS.')
            for item in range(len(clause_6_p1)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_6_p1[item])
                y_aux += 20
            c.drawCentredString(x=w / 2, y=50, text='5')
            c.showPage()

            # CLAUSE 6, 7 & 8 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause_6_p2 = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_6_P2)
            clause_7 = Helpers.generic_clause_split(clause=constants.CLAUSE_7)
            clause_8_p1 = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_8_P1)
            clause_8_p2 = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_8_P2)
            for item in range(len(clause_6_p2)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_6_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='SÉPTIMA. INTERESES MORATORIOS.')
            for item in range(len(clause_7)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_7[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='OCTAVA. AMORTIZACIÓN.')
            for item in range(len(clause_8_p1)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_8_p1[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='Banco: {bank}'.format(bank=contract['bank']))
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='Clabe interbancaria: {clabe}'.format(clabe=contract['clabe']))
            y_aux += 10
            for item in range(len(clause_8_p2)):
                if item == 0:
                    y_aux += 20
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_8_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='NOVENA. CONSIDERACIONES FISCALES.')
            c.drawCentredString(x=w / 2, y=50, text='6')
            c.showPage()

            # CLAUSE 9, 10 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_9_P1)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_9_P2)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='DÉCIMA. DERECHOS Y OBLIGACIONES DE LAS PARTES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_10_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    10.1    Derechos y Obligaciones del Acreedor.')
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='El Acreedor tendrá los siguientes derechos y obligaciones:')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_10_1_A)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_10_1_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    10.2    Derechos y Obligaciones del Deudor.')
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='El Deudor tendrá los siguientes derechos y obligaciones:')
            clause = Helpers.clause_3_split(clause=constants.CLAUSE_10_2_A, written_amount=contract['written_amount'], number_amount=contract['number_amount'])
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_10_2_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w / 2, y=50, text='7')
            c.showPage()

            # CLAUSE 11, 12 & 13 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO PRIMERA.    VENCIMIENTO ANTICIPADO.')
            clause = Helpers.generic_clause_split(clause=constants.STANDARD_CLAUSE_11)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_11_A)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_11_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SEGUNDA.    CESIÓN Y BENEFICIARIO.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_12_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_12_P2)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Nombre del Beneficiario: {}'.format(contract['beneficiary_name']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Correo electrónico: {}'.format(contract['beneficiary_email']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Número de teléfono: {}'.format(contract['beneficiary_phone']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Relación con el Acredor: {}'.format(contract['beneficiary_relationship']))
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO TERCERA.    GASTOS Y COSTAS.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_13_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_13_P2)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w / 2, y=50, text='8')
            c.showPage()

            # CLAUSE 14, 15, 16 & 17 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO CUARTA.    MODIFICACIONES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_14)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO QUINTA.    DOMICILIOS Y NOTIFICACIONES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_15_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            c.drawString(x=constants.LEFT_PADDING + 40, y=new_y_statement - y_aux,
                         text='Acreedor')
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='{}'.format(contract['creditor']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Tel.{}'.format(contract['creditor_phone']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Atención: {}'.format(contract['creditor_atention']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='E-mail: {}'.format(contract['creditor_email']))
            y_aux += 20
            c.drawString(x=constants.LEFT_PADDING + 40, y=new_y_statement - y_aux,
                         text='Acreditado')
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Naica Technologies, S.A. de C.V.')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Avenida Santa Fe #505, Piso 1, interior 2B,')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Colonia Santa Fe, Delegación Cuajimalpa')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='de Morelos, CP 05348, CDMX, México.')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Tel: 800 624 2200')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Atención: Pamela Larraguivel Alemán')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='E-mail: contratos@naica.mx')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_15_P2)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SEXTA.    LEGISLACIÓN APLICABLE Y JURISDICCIÓN.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_16)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SÉPTIMA.    INTEGRIDAD DEL CONTRATO.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_17_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            c.drawCentredString(x=w / 2, y=50, text='9')
            c.showPage()

            # CLAUSE 17 & 18 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text=constants.CLAUSE_17_P2)
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO OCTAVA.    RENUNCIA.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_18)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=constants.WHITE_SPACE_TOP)
            y_aux += 12
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=constants.WHITE_SPACE_BOTTOM)

            c.drawCentredString(x=w / 2, y=50, text='10')
            c.showPage()

            # SIGNATURE --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause = Helpers.signature_header_split(day=day, month=month, year=year)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text='ACREEDOR')
            y_aux += 12
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=contract['creditor'])
            y_aux += 50
            c.line(x1=(w/2)-100, x2=(w/2)+100, y1=new_y_statement - y_aux, y2=new_y_statement - y_aux)
            y_aux += 12
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='Por su propio derecho')
            y_aux += 40
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='DEUDOR')
            y_aux += 12
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='NAICA TECHNOLOGIES, S.A. DE C.V.')
            y_aux += 50
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Por:')
            c.line(x1=(w/3)+25, x2=(w/2)+100, y1=new_y_statement - y_aux, y2=new_y_statement - y_aux)
            y_aux += 12
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Nombre: Héctor Augusto Muñoz Vences')
            y_aux += 12
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Cargo: Representante Legal')
            c.drawCentredString(x=w / 2, y=50, text='11')
            c.showPage()


            print(len('CONTRATO DE CRÉDITO SIMPLE CON INTERÉS QUE CELEBRAN POR UNA PARTE'))



            c.save()
            return {
                'success': True,
                'message': 'CONTRATO CREADO'
            }

        except Exception as e:
            print(e)
            return {
                'success': False,
                'message': e
            }

    @staticmethod
    def generate_dynamic_contract(contract):
        try:
            # PDF CONFIGURATIONS ------------------------------------------------------------------
            w, h = letter
            day, month, year = Helpers.get_today_date()
            contract_type = constants.CONTRACT_TYPE['{}'.format(contract['contract_type'])]
            c = canvas.Canvas('{}.pdf'.format(contract['creditor']), pagesize=letter)
            c.setTitle('Contrato {ct} {cc}'.format(ct=contract_type, cc=contract['creditor']))


            # PDF MAIN PAGE -----------------------------------------------------------------------
            c.drawCentredString(x=w/2, y=(h/2)+300, text='CONTRATO DE CRÉDITO SIMPLE CON INTERÉS')
            c.drawCentredString(x=w/2, y=(h/2)+220, text='ENTRE')
            c.drawCentredString(x=w/2, y=(h/2)+140, text='{}'.format(contract['creditor'].upper()))
            c.drawCentredString(x=w/2, y=(h/2)+120, text='COMO ACREEDOR')
            c.drawCentredString(x=w/2, y=(h/2)+80, text='Y')
            c.drawCentredString(x=w/2, y=(h/2)+50, text='NAICA TECHNOLOGIES, S.A. DE C.V.')
            c.drawCentredString(x=w/2, y=(h/2)+30, text='COMO DEUDOR')
            c.drawCentredString(x=w/2, y=(h/2)-290,
                                text='{day} DE {month} DE {year}'.format(
                                day=day, month=month, year=year))
            c.showPage()


            # PDF STATEMENTS ------------------------------------------------------------------------
            statement = Helpers.statement_split(creditor=contract['creditor'])
            y_statement = 320
            for statement_line in statement:
                c.drawString(x=constants.LEFT_PADDING, y=(h/2)+y_statement, text=statement_line)
                y_statement -= 15
            new_y_statement = (h/2)+y_statement
            c.drawCentredString(x=w/2, y=new_y_statement-20, text='DECLARACIONES')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-50,
                         text='I.    Declara el Acreedor por conducto de su representante legal:')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-80,
                         text='    1.    Que es una persona física, mayor de edad, en pleno uso de sus facultades;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-110,
                         text='    2.    Que de conformidad con la regulación aplicable mantiene los requisitos necesarios')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-130,
                         text='para ser considerado un inversionista calificado;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='    3.    Que es su voluntad celebrar el presente Contrato y obligarse en los términos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='establecidos;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 210,
                         text='    4.    Que el presente Contrato constituye obligaciones legales, válidas y obligatorias del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='Acreedor, exigibles de conformidad con los términos y condiciones establecidos en el')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='presente;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 280,
                         text='    5.    Que todas las declaraciones contenidas en este Contrato son ciertas, correctas y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='verdaderas en esta fecha;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 330,
                         text='    6.    Que no existe ni tiene conocimiento de que pudiere existir o iniciarse en el futuro')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 350,
                         text='alguna acción, demanda, reclamación, requerimiento o procedimiento judicial o')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 370,
                         text='extrajudicial que afecte o pudiere afectar la legalidad, validez o exigibilidad del presente')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 390,
                         text='Contrato;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 420,
                         text='    7.    Que cuenta con Registro Federal de Contribuyentes número: {rfc}; y'.format(rfc=contract['rfc']))
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 450,
                         text='    8.    Que está dispuesta a transferir la propiedad de una suma de dinero solicitado')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 470,
                         text='por el Deudor y que cuenta con los recursos necesarios para ello, de acuerdo con los')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 490,
                         text='términos y bajo las condiciones establecidas en el presente Contrato y que dichos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 510,
                         text='recursos provienen de actividades lícitas.')
            c.drawCentredString(x=w/2, y=50, text='2')
            c.showPage()

            # PDF STATEMENTS P2 ------------------------------------------------------------------------
            new_y_statement = (h/2)+320
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement,
                         text='II.    Declara el Deudor por conducto de su representante legal:')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-30,
                         text='    1.    Que es una persona moral de nacionalidad mexicana, lo cual acredita con la')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-50,
                         text='escritura pública número 29,187 de fecha veinticinco días del mes de agosto del año dos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 70,
                         text='mil dieciséis, otorgada ante la fe del licenciado José Antonio Acosta Pérez, titular de la')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 90,
                         text='Notaría Pública número Nueve y del Patrimonio Inmobiliario Federal de la ciudad de ')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 110,
                         text='Cuernavaca, Morelos, la cual se encuentra debidamente inscrita ante el Registro Público ')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 130,
                         text='de la Propiedad y del Comercio de Cuernavaca bajo el folio mercantil número 2016024035;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='    2.    Que es su voluntad celebrar el presente Contrato y obligarse en los términos en él')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='establecidos y que conforme a su objeto social puede llevar a cabo la celebración del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 200,
                         text='presente Contrato;')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='    3.    Que el presente Contrato constituye obligaciones legales, válidas y obligatorias del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='Deudor, exigibles de conformidad con los términos y condiciones establecidos en el')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 270,
                         text='presente.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='    4.    Que todas las declaraciones contenidas en este Contrato son ciertas, correctas y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 320,
                         text='verdaderas en esta fecha.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 350,
                         text='    5.    Que no existe ni tiene conocimiento de que pudiere existir o iniciarse en el futuro')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 370,
                         text='alguna acción, demanda, reclamación, requerimiento o procedimiento judicial o')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 390,
                         text='extrajudicial que afecte o pudiere afectar la legalidad, validez o exigibilidad del')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 410,
                         text='presente Contrato.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 440,
                         text='    6.    Que cuenta con Registro Federal de Contribuyentes número: NTE160825PG2.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 470,
                         text='    En virtud de lo anterior, las Partes acuerdan en obligarse de conformidad con las')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 490,
                         text='siguientes:')
            c.drawCentredString(x=w/2, y=new_y_statement-520, text='C L Á U S U L A S')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement-550, text='PRIMERA. DEFINICIONES .')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 570,
                         text='    Los términos con mayúscula inicial utilizados en el presente Contrato que no se')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 590,
                         text='encuentren definidos de otra manera, tendrán el significado que se atribuye a dichos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 610,
                         text='términos en la presente Cláusula y serán utilizados en forma singular o plural según')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 630,
                         text='sea aplicable.')
            c.drawCentredString(x=w / 2, y=50, text='3')
            c.showPage()

            # PDF CLAUSES & CLAUSE 2---------------------------------------------------------------------------------
            # --- TABLE START ---
            creditor_condition = ['“Acreedor”', 'Significa el señor(a) {}'.format(contract['creditor'])]
            new_y_statement = (h / 2) + 70
            clauses_table_data = constants.DYNAMIC_CLAUSES_DATA
            clauses_table_data.insert(0, creditor_condition)
            clauses_table_data.insert(0, constants.CLAUSES_TABLE_HEADER)
            table = Table(clauses_table_data)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#000066')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOX', (0, 0), (-1, -1), 1, HexColor('#000000')),
                ('GRID', (0, 1), (-1, -1), 1, HexColor('#000000')),
                ('VALIGN', (0,0), (-1, -1), 'MIDDLE')
            ])
            table.setStyle(style)
            table._argW[0] = (w / 10) * 2
            table._argW[1] = (w / 10) * 5.5
            table.wrapOn(c, 0, 0)
            table.drawOn(c, x=constants.LEFT_PADDING, y=new_y_statement)
            # --- TABLE END ---
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 40, text='SEGUNDA. INTERPRETACIÓN INTEGRAL DEL CONTRATO.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 70,
                         text='    Las Partes acuerdan que las declaraciones, definiciones, cláusulas y anexos de este')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 90,
                         text='Contrato, son parte integrante del presente Contrato de Crédito.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 120,
                         text='    Las palabras, “del presente”, “en el presente” y “conforme al presente”, y las palabras')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 140,
                         text='de significado similar siempre que sean utilizadas en este Contrato se referirán a este')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 160,
                         text='Contrato en su totalidad y no a disposiciones en específico del mismo. Los términos')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 180,
                         text='cláusula, declaración y anexo se refieren a las Cláusulas, Declaraciones y Anexos de')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 200,
                         text='este Contrato, salvo que se especifique lo contrario.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 230,
                         text='    Las referencias a cualquier Persona o Personas se interpretarán como referencias a')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 250,
                         text='cualesquiera sucesores o cesionarios de esa Persona o Personas.')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 280,
                         text='    Los títulos que aparecen en cada una de las cláusulas son exclusivamente para')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 300,
                         text='facilitar su lectura y, por consiguiente, no se considerará que definen, limitan o describen')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 320,
                         text='el contenido de las cláusulas del mismo, ni para efectos de su interpretación y')
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - 340,
                         text='cumplimiento.')
            c.drawCentredString(x=w / 2, y=50, text='4')
            c.showPage()

            # CLAUSE 3, 4, 5 & 6 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            splited_clause_3 = Helpers.clause_3_split(clause=constants.CLAUSE_3, written_amount=contract['written_amount'], number_amount=contract['number_amount'])
            splited_clause_3_p2 = Helpers.generic_clause_split(clause=constants.CLAUSE_3_P2)
            clause_4 = Helpers.generic_clause_split(clause=constants.CLAUSE_4)
            clause_5_p1 = Helpers.standard_clause_5_split(
                clause=constants.DYNAMIC_CLAUSE_5_P1,
                written_deadline_days=contract['written_deadline_days'],
                number_deadline_days=contract['number_deadline_days'],
                deadline_date=contract['deadline_date']
            )
            clause_5_p2 = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_5_P2)
            y_aux = 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement, text='TERCERA. CRÉDITO SIMPLE.')
            for item in range(len(splited_clause_3)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement-y_aux, text=splited_clause_3[item])
                y_aux += 20

            for item in range(len(splited_clause_3_p2)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=splited_clause_3_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='CUARTA. DESTINO DE LOS FONDOS.')
            for item in range(len(clause_4)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_4[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='QUINTA.    PLAZO Y AMORTIZACIÓN.')
            for item in range(len(clause_5_p1)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_5_p1[item])
                y_aux += 20
            for item in range(len(clause_5_p2)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_5_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='SEXTA. INTERESES ORDINARIOS.')
            c.drawCentredString(x=w / 2, y=50, text='5')
            c.showPage()

            # CLAUSE 6, 7 & 8 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause_6_p1 = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_6_P1)
            clause_6_p2 = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_6_P2)
            clause_7 = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_7)
            clause_8 = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_8)
            for item in range(len(clause_6_p1)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_6_p1[item])
                y_aux += 20
            for item in range(len(clause_6_p2)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_6_p2[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='SÉPTIMA. INTERESES MORATORIOS.')
            for item in range(len(clause_7)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_7[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='OCTAVA. AMORTIZACIÓN.')
            for item in range(len(clause_8)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause_8[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='Banco: {bank}'.format(bank=contract['bank']))
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='Clabe interbancaria: {clabe}'.format(clabe=contract['clabe']))
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='NOVENA. CONSIDERACIONES FISCALES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_9_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            c.drawCentredString(x=w / 2, y=50, text='6')
            c.showPage()

            # CLAUSE 9, 10 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_9_P2)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 10
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux, text='DÉCIMA. DERECHOS Y OBLIGACIONES DE LAS PARTES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_10_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    10.1    Derechos y Obligaciones del Acreedor.')
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='El Acreedor tendrá los siguientes derechos y obligaciones:')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_10_1_A)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_10_1_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    10.2    Derechos y Obligaciones del Deudor.')
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='El Deudor tendrá los siguientes derechos y obligaciones:')
            clause = Helpers.clause_3_split(clause=constants.CLAUSE_10_2_A, written_amount=contract['written_amount'], number_amount=contract['number_amount'])
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_10_2_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w / 2, y=50, text='7')
            c.showPage()

            # CLAUSE 11, 12 & 13 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO PRIMERA.    VENCIMIENTO ANTICIPADO.')
            clause = Helpers.generic_clause_split(clause=constants.DYNAMIC_CLAUSE_11)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_11_A)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_11_B)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SEGUNDA.    CESIÓN Y BENEFICIARIO.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_12_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_12_P2)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Nombre del Beneficiario: {}'.format(contract['beneficiary_name']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Correo electrónico: {}'.format(contract['beneficiary_email']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Número de teléfono: {}'.format(contract['beneficiary_phone']))
            y_aux += 12
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='    Relación con el Acredor: {}'.format(contract['beneficiary_relationship']))
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO TERCERA.    GASTOS Y COSTAS.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_13_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_13_P2)
            for item in range(len(clause)):
                if item == 0:
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w / 2, y=50, text='8')
            c.showPage()

            # CLAUSE 14, 15, 16 & 17 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO CUARTA.    MODIFICACIONES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_14)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO QUINTA.    DOMICILIOS Y NOTIFICACIONES.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_15_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            c.drawString(x=constants.LEFT_PADDING + 40, y=new_y_statement - y_aux,
                         text='Acreedor')
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='{}'.format(contract['creditor']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Tel.{}'.format(contract['creditor_phone']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Atención: {}'.format(contract['creditor_atention']))
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='E-mail: {}'.format(contract['creditor_email']))
            y_aux += 20
            c.drawString(x=constants.LEFT_PADDING + 40, y=new_y_statement - y_aux,
                         text='Deudor')
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Naica Technologies, S.A. de C.V.')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Avenida Santa Fe #505, Piso 1, interior 2B,')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Colonia Santa Fe, Delegación Cuajimalpa')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='de Morelos, CP 05348, CDMX, México.')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Tel: 800 624 2200')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='Atención: Pamela Larraguivel Alemán')
            y_aux += 12
            c.drawString(x=w / 2, y=new_y_statement - y_aux,
                         text='E-mail: contratos@naica.mx')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_15_P2)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SEXTA.    LEGISLACIÓN APLICABLE Y JURISDICCIÓN.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_16)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO SÉPTIMA.    INTEGRIDAD DEL CONTRATO.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_17_P1)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            c.drawCentredString(x=w / 2, y=50, text='9')
            c.showPage()

            # CLAUSE 17 & 18 --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text=constants.CLAUSE_17_P2)
            y_aux += 30
            c.drawString(x=constants.LEFT_PADDING, y=new_y_statement - y_aux,
                         text='DÉCIMO OCTAVA.    RENUNCIA.')
            clause = Helpers.generic_clause_split(clause=constants.CLAUSE_18)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=constants.WHITE_SPACE_TOP)
            y_aux += 12
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=constants.WHITE_SPACE_BOTTOM)

            c.drawCentredString(x=w / 2, y=50, text='10')
            c.showPage()

            # SIGNATURE --------------------------------------------------------------------------------------
            new_y_statement = (h / 2) + 320
            y_aux = 0
            clause = Helpers.signature_header_split(day=day, month=month, year=year)
            for item in range(len(clause)):
                if item == 0:
                    y_aux += 30
                    x_padding = constants.LEFT_PADDING + 15
                else:
                    x_padding = constants.LEFT_PADDING
                c.drawString(x=x_padding, y=new_y_statement - y_aux, text=clause[item])
                y_aux += 20
            y_aux += 10
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text='ACREEDOR')
            y_aux += 12
            c.drawCentredString(x=w/2, y=new_y_statement - y_aux, text=contract['creditor'])
            y_aux += 50
            c.line(x1=(w/2)-100, x2=(w/2)+100, y1=new_y_statement - y_aux, y2=new_y_statement - y_aux)
            y_aux += 12
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='Por su propio derecho')
            y_aux += 40
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='DEUDOR')
            y_aux += 12
            c.drawCentredString(x=w / 2, y=new_y_statement - y_aux, text='NAICA TECHNOLOGIES, S.A. DE C.V.')
            y_aux += 50
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Por:')
            c.line(x1=(w/3)+25, x2=(w/2)+100, y1=new_y_statement - y_aux, y2=new_y_statement - y_aux)
            y_aux += 12
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Nombre: Héctor Augusto Muñoz Vences')
            y_aux += 12
            c.drawString(x=w/3 , y=new_y_statement - y_aux, text='Cargo: Representante Legal')
            c.drawCentredString(x=w / 2, y=50, text='11')
            c.showPage()


            print(len('CONTRATO DE CRÉDITO SIMPLE CON INTERÉS QUE CELEBRAN POR UNA PARTE'))



            c.save()
            return {
                'success': True,
                'message': 'CONTRATO CREADO'
            }

        except Exception as e:
            print(e)
            return {
                'success': False,
                'message': e
            }
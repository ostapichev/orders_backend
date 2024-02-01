from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.workbook import Workbook

from configs.extra_conf import desired_column_order, column_widths


class ExportFileService:
    @classmethod
    def __table_style(cls, df, sheet):
        cls.__create_header(sheet)
        for row_index, row in enumerate(df.itertuples(), start=2):
            if row_index % 2 == 0:
                for column_index in range(1, len(desired_column_order) + 1):
                    cell = sheet.cell(row=row_index, column=column_index)
                    cell.fill = PatternFill(start_color='E9E9E9', end_color='E9E9E9', fill_type='solid')
            for column_index, column_name in enumerate(desired_column_order, start=1):
                value = getattr(row, column_name)
                cell = sheet.cell(row=row_index, column=column_index, value=value)
                cell.alignment = Alignment(horizontal='center', vertical='center')
                width = column_widths.get(column_name, 12)
                sheet.column_dimensions[sheet.cell(row=1, column=column_index).column_letter].width = width

    @staticmethod
    def __create_header(sheet):
        for column_index, column_name in enumerate(desired_column_order, start=1):
            cell = sheet.cell(row=1, column=column_index, value=column_name)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.fill = PatternFill(start_color='50C878', end_color='50C878', fill_type='solid')
            cell.font = Font(color='FFFFFF')

    @staticmethod
    def date_converter(data):
        for item in data:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = timezone.localtime(value).replace(tzinfo=None)

    @staticmethod
    def name_creator():
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        return f'{formatted_datetime}.xlsx'

    @classmethod
    def book_creator(cls, df, filename):
        try:
            workbook = Workbook()
            sheet = workbook.active
            excel_buffer = BytesIO()
            cls.__table_style(df, sheet)
            workbook.save(excel_buffer)
            excel_buffer.seek(0)
            excel_buffer_content = excel_buffer.getvalue()
            response = HttpResponse(
                excel_buffer_content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        except Exception as e:
            return Response({'error exel book creator': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

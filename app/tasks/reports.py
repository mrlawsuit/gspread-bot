from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime, timedelta, UTC
from ..models import VehicleMaintenance


def create_report(filename, maintenances):
    # Регистрируем шрифт, поддерживающий кириллицу
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    # Регистрация жирного шрифта
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

    pdf_catalog = f'/pdf_files/{filename}.pdf'

    # Создаем объект canvas с размером страницы A4
    page = canvas.Canvas(pdf_catalog, pagesize=A4)
    width, height = A4  # Ширина и высота страницы A4

    # Начальная позиция
    y_position = height - 50

    # Заголовок
    title = f'Отчет об обслуживании автомобилей в период с {datetime.now(UTC) - timedelta(days=30)} по {datetime.now(UTC)}'
    y_position -= 150
    # Установка жирного шрифта
    page.setFont('DejaVuSans-Bold', 12)

    for row in title.split('\n'):
        page.drawString(120, y_position, row)

    body = f'За последний месяц было обслужено {len(maintenances)} автомобилей:'
    for maintenance in maintenances:
        record = f'\n{maintenance.vehicle_id}, дата обслуживания {maintenance.service_date}, пробег на момент обслуживания {maintenance.current_mileage}'
        body += record

    # Устанавливаем шрифт и размер
    page.setFont('DejaVuSans', 12)
    if y_position > 50:
        for row in body.split('\n'):
            # Добавляем текст после изображения
            y_position -= 50  # Смещаем позицию для текста после изображения
            page.drawString(50, y_position,  row)
            y_position -= 15
            if y_position < 50:
                page.showPage()
                y_position = 800
                page.setFont('DejaVuSans', 12)

    else:
        page.showPage()
        y_position = 800

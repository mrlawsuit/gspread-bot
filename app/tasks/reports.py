from datetime import datetime, timedelta, UTC

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Frame, Paragraph

from ..repositories import maintenances_repository, vehicles_repository


async def maintenance_report():

    maintenances = await maintenances_repository.get_maintenances_per_month()
    title = f'Отчет об обслуживании автомобилей в период с {
            (datetime.now(UTC) - timedelta(days=30)).strftime('%d-%m-%Y')
        } по {datetime.now(UTC).strftime('%d-%m-%Y')}'

    body = (
            f'<br/>За последний месяц '
            f'было обслужено {len(maintenances)} автомобилей:<br/>'
        )
    for maintenance in maintenances:
        print(f'проверка {maintenance}')
        print(f'проверка 2 {maintenances}')
        vehicle = await vehicles_repository.get_vehicle_by_id(maintenance.vehicle_id)
        record = (
            f'<br/><br/>{vehicle.brand} {vehicle.model}. '
            f'Регистрационный знак - "{vehicle.plate}".'
            f'<br/>Дата обслуживания - {maintenance.service_date.strftime('%d-%m-%Y')}, '
            f'пробег на момент обслуживания - {maintenance.current_mileage} километров'
        )
        body += record
    return {'title': title, 'body': body}

def create_report(filename, title, body):
    # Регистрируем шрифт, поддерживающий кириллицу
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

    pdf_catalog = f'{filename}.pdf'

    # Создаем объект canvas с размером страницы A4
    page = canvas.Canvas(pdf_catalog, pagesize=A4)
    width, height = A4  # Ширина и высота страницы A4

    # Начальная позиция
    y_position = height - 100

    # установка ограничения по полям
    frame = Frame(50, 50, width - 150, y_position, showBoundary=0)

    # добавляем стили для кирилицы
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='RussianStyle',
        parent=styles['BodyText'],
        fontName='DejaVuSans'
    ))
    styles.add(ParagraphStyle(
        name='RussianStyleBold',
        parent=styles['Title'],
        fontName='DejaVuSans-Bold'
    ))

    content = [Paragraph(title, styles['RussianStyleBold'])]
    content.append(Paragraph(body, styles['RussianStyle']))

    frame.addFromList(content, page)

    page.save()

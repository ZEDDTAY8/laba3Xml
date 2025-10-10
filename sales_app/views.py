from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import SaleForm
import os
import uuid
import xml.etree.ElementTree as ET

def index(request):
    form = SaleForm()
    xml_files = []
    xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    if os.path.exists(xml_dir):
        xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    
    xml_contents = []
    for file in xml_files:
        try:
            tree = ET.parse(os.path.join(xml_dir, file))
            root = tree.getroot()
            sales = []
            for sale in root.findall('sale'):
                data = {
                    'id': sale.get('id'),
                    'product': sale.find('product').text if sale.find('product') is not None else '',
                    'price': sale.find('price').text if sale.find('price') is not None else '',
                    'quantity': sale.find('quantity').text if sale.find('quantity') is not None else '',
                    'date': sale.find('date').text if sale.find('date') is not None else '',
                }
                sales.append(data)
            xml_contents.append({'file': file, 'sales': sales})
        except ET.ParseError:
            xml_contents.append({'file': file, 'error': 'Невалидный XML'})

    context = {'form': form, 'xml_contents': xml_contents, 'has_files': bool(xml_files)}
    return render(request, 'sales_app/index.html', context)

def save_to_xml(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
            os.makedirs(xml_dir, exist_ok=True)
            file_name = f"sale_{uuid.uuid4()}.xml"
            file_path = os.path.join(xml_dir, file_name)

            root = ET.Element('sales')
            sale = ET.SubElement(root, 'sale', id=str(uuid.uuid4()))
            ET.SubElement(sale, 'product').text = data['product']
            ET.SubElement(sale, 'price').text = str(data['price'])
            ET.SubElement(sale, 'quantity').text = str(data['quantity'])
            ET.SubElement(sale, 'date').text = data['date'].strftime('%Y-%m-%d')

            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            return redirect('sales_app:index')
    return redirect('sales_app:index')

def upload_xml(request):
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xml_file = request.FILES['xml_file']
        if xml_file.name.endswith('.xml'):
            # Санитайзинг имени: генерируем новое
            file_name = f"uploaded_{uuid.uuid4()}.xml"
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'xml_files'))
            path = fs.save(file_name, xml_file)
            full_path = os.path.join(settings.MEDIA_ROOT, 'xml_files', file_name)

            # Валидация: пытаемся парсить
            try:
                ET.parse(full_path)
            except ET.ParseError:
                os.remove(full_path)
                # Сообщение об ошибке
                return render(request, 'sales_app/index.html', {'error': 'Невалидный XML-файл. Файл удалён.'})
        else:
            return render(request, 'sales_app/index.html', {'error': 'Только XML-файлы.'})
    return redirect('sales_app:index')
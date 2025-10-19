from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
import os
import uuid
import xml.etree.ElementTree as ET

# Список полей для формы, XML и отображения
FIELDS = [
    {'name': 'product', 'label': 'Товар', 'type': 'str', 'max_length': 100},
    {'name': 'price', 'label': 'Цена', 'type': 'float', 'min_value': 0},
    {'name': 'quantity', 'label': 'Количество', 'type': 'int', 'min_value': 1},
    {'name': 'date', 'label': 'Дата продажи', 'type': 'date'},
]

# Динамическая форма
def create_sale_form():
    class SaleForm(forms.Form):
        for field in FIELDS:
            if field['type'] == 'str':
                locals()[field['name']] = forms.CharField(max_length=field.get('max_length', 100), label=field['label'])
            elif field['type'] == 'float':
                locals()[field['name']] = forms.FloatField(min_value=field.get('min_value', 0), label=field['label'])
            elif field['type'] == 'int':
                locals()[field['name']] = forms.IntegerField(min_value=field.get('min_value', 1), label=field['label'])
            elif field['type'] == 'date':
                locals()[field['name']] = forms.DateField(label=field['label'], widget=forms.DateInput(attrs={'type': 'date'}))
            elif field['type'] == 'bool':
                locals()[field['name']] = forms.BooleanField(label=field['label'], required=False) 
    return SaleForm

def index(request):
    form = create_sale_form()()  
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
                data = {'id': sale.get('id')}
                for field in FIELDS:
                    text_value = sale.find(field['name']).text if sale.find(field['name']) is not None else ''
                    if field['type'] == 'bool':
                        data[field['name']] = text_value.lower() == 'true' 
                    else:
                        data[field['name']] = text_value
                sales.append(data)
            xml_contents.append({'file': file, 'sales': sales})
        except ET.ParseError:
            xml_contents.append({'file': file, 'error': 'Невалидный XML'})

    context = {'form': form, 'xml_contents': xml_contents, 'has_files': bool(xml_files), 'fields': FIELDS}
    return render(request, 'sales_app/index.html', context)

def save_to_xml(request):
    if request.method == 'POST':
        form = create_sale_form()(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
            os.makedirs(xml_dir, exist_ok=True)
            file_name = f"sale_{uuid.uuid4()}.xml"
            file_path = os.path.join(xml_dir, file_name)

            root = ET.Element('sales')
            sale = ET.SubElement(root, 'sale', id=str(uuid.uuid4()))
            for field in FIELDS:
                value = data.get(field['name'])
                if value is not None:
                    if field['type'] == 'bool':
                        ET.SubElement(sale, field['name']).text = 'true' if value else 'false'  # Сохраняем как текст
                    else:
                        ET.SubElement(sale, field['name']).text = str(value) if field['type'] != 'date' else value.strftime('%Y-%m-%d')

            tree = ET.ElementTree(root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            return redirect('sales_app:index')
    return redirect('sales_app:index')

def upload_xml(request):
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xml_file = request.FILES['xml_file']
        if xml_file.name.endswith('.xml'):
            file_name = f"uploaded_{uuid.uuid4()}.xml"
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'xml_files'))
            path = fs.save(file_name, xml_file)
            full_path = os.path.join(settings.MEDIA_ROOT, 'xml_files', file_name)

            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                if root.tag != 'sales':
                    os.remove(full_path)
                    return render(request, 'sales_app/index.html', {'error': 'Невалидный XML: ожидается корневой тег <sales>'})
                for sale in root.findall('sale'):
                    if not all(sale.find(field['name']) is not None for field in FIELDS):
                        os.remove(full_path)
                        return render(request, 'sales_app/index.html', {'error': 'Невалидный XML: отсутствуют обязательные поля'})
            except ET.ParseError:
                os.remove(full_path)
                return render(request, 'sales_app/index.html', {'error': 'Невалидный XML-файл. Файл удалён.'})
        else:
            return render(request, 'sales_app/index.html', {'error': 'Только XML-файлы.'})
    return redirect('sales_app:index')
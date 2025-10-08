import os 
import uuid 
import xml.etree.ElementTRee as ET
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import SaleForm

def index(request):
    form = SaleForm()
    xml_files = []
    xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml_files')
    if os.path.exist(xml_dir):
        xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]

    xml_content = []
    for file in xml_files:
        try:
            tree = ET.parse(os.path(xml_dir, file))
            root = tree.hetroot()
            sales = []
            for sale in root.findall('sale'):
                data = {
                    'id': sale.get('id'),
                    'product' sale.find('product').text if sale.find
                    'price' sale.find
                    'quantity' sale.find
                    'date' sale.find
                }

# Create your views here.

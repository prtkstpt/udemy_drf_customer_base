from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Customer, DataSheet, Document, Profession
from .serializer import (CustomerSerializer, DataSheetSerializer,
                         DocumentSerializer, ProfessionSerializer)


class CustomerViewSet(viewsets.ModelViewSet):
    
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        active_customers = Customer.objects.filter(active=True)
        return active_customers
    
    
    def list(self, request, *args, **kwargs):
        customers= Customer.objects.filter(id=2)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name = data['name'], address = data['address'],
            data_sheet_id = data['data_sheet'],
            )
        profession = Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']           
        print('prffffffff', data['profession'])
        profession = Profession.objects.get(id=data['profession'])
        
        for p in customer.professions.all():
            customer.professions.remove(p)
        
        customer.professions.add(profession)
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
        
        
class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

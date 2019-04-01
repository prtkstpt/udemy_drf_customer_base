from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


from .models import Customer, DataSheet, Document, Profession
from .serializer import (CustomerSerializer, DataSheetSerializer,
                         DocumentSerializer, ProfessionSerializer)


class CustomerViewSet(viewsets.ModelViewSet):
    
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name',)
    search_fields = ('name', 'address', 'data_sheet__description')
    ordering_fields = ('id', 'name')
    ordering = ('id')
    
    def get_queryset(self):
        address = self.request.query_params.get('address', None)
        status = False if self.request.query_params.get('active') == 'False' else True
        
        if address:
            customers = Customer.objects.filter(address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)
        return customers
    
    """
    def list(self, request, *args, **kwargs):
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    """
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
        
        
    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response('Object Removed')
        
    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
        
    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['active'] == 'True' else False 
        customers = self.get_queryset()
        customers.update(active=status)
        
        serializer = CustomerSerializer(customers, many=True)
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

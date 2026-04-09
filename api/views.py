from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['get'])
def Home(request):
    return Response({'message':'multivendor hotel management system is running'})
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, mixins
from ratings import *
from .models import User
from .serializers import UserSerializer

# Create your views here.

class BusinessDetails(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):

        data = request.data
        pincode = data.get('pincode')
        state = data.get('state')
        district = data.get('district')
        typeOfBusiness = data.get('typeofbusiness') or None

        competitorAnalysis = competitor_analysis(pincode)
        oppurtunityRating = oppurtunity_rating(state,district)
        sectoralAnalysis = sectoral_analysis(typeOfBusiness)
        relativeProsperity = relative_prosperity(state,district)
        easeOfBusiness = ease_of_business(pincode, state)

        return Response({
            "competitorAnalysis": competitorAnalysis,
            "oppurtunityRating": oppurtunityRating,
            "sectoralAnalysis": sectoralAnalysis,
            "relativeProsperity": relativeProsperity,
            "easeOfBusiness": easeOfBusiness
        })

class UserView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if User.objects.filter(mobile=request.data['mobile']).exists():
            User.objects.get(mobile=request.data['mobile']).name=request.data['name']
            User.objects.get(mobile=request.data['mobile']).save()
            return Response(UserSerializer(instance=User.objects.get(mobile=request.data['mobile'])).data)
        else:
            return super().post(request, *args, **kwargs)
    
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, mixins
# from ratings import *
from .models import User
from .serializers import UserSerializer

# Create your views here.

class BusinessDetails(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):

        data = request.data
        pincode = data.get('pincode')
        state = data.get('state')
        district = data.get('district')
        typeOfBusiness = data.get('typeofbusiness')

        competitorAnalysis = competitor_analysis(pincode)
        oppurtunityRating = oppurtunity_rating(state,district)
        sectoralAnalysis = sectoral_analysis(typeOfBusiness.lower())
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
    
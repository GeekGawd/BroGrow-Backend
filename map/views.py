from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, mixins
from ratings import *
from .models import User
from .serializers import UserSerializer
import pickle
import random

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

def credit_score(df):
    try:
        model=pickle.load(open("Credit-Model\Credit_Risk_Model_and_Credit_Scorecard.ipynb", 'rb'))
        y_pred = model.predict(df) 
        y_pred=(y_pred>0.80) 
        result = "Yes" if y_pred else "No"
        return result 
    except ValueError as e: 
        return e.args[0]

class BroScrView(generics.GenericAPIView):
    def post(self, request):

        data = request.data
        pincode = data.get('pincode')
        state = data.get('state')
        district = data.get('district')
        typeOfBusiness = data.get('typeofbusiness') or None

        competitorScore = competitor_analysis(pincode)['rating']
        oppurtunityScore = oppurtunity_rating(state,district)['rating']
        sectoralScore = sectoral_analysis(typeOfBusiness)['rating']
        relativeScore = relative_prosperity(state,district)['rating']
        easeOfBusiness = ease_of_business(pincode, state)['rating']

        scr=competitorScore+oppurtunityScore+sectoralScore+relativeScore+easeOfBusiness
        if 'Payload' in data.keys():
            bal = float(data['Payload'][0]['data'][0]['decryptedFI']['account']['summary']['currentBalance'])
        else:
            bal = 50468.68
        return Response({'BroScore':Score(scr, bal)})


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, mixins
from ratings import *
from .models import User, LoanApplication
from .serializers import UserSerializer, LoanApplicationSerializer
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

class LoanApplicationView(generics.GenericAPIView,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin):
    serializer_class = LoanApplicationSerializer
    model = LoanApplication

    def get_queryset(self):
        query = self.request.query_params.get('approve', None)

        id = self.request.query_params.get('id', None)

        if id is not None:
            return LoanApplication.objects.filter(id = id).first()

        q = self.model.objects.all()

        if query == "true":
            q = q.filter(status=True)

        elif query == "false":
            q = q.filter(status=False)
        
        return q
    
    def get_object(self):
        id = self.request.query_params.get('id', None)

        if id is not None:
            return LoanApplication.objects.filter(id = id).first()

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        queryset = self.model.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
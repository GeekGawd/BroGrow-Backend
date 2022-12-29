from .models import User, LoanApplication
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

class LoanApplicationSerializer(ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'


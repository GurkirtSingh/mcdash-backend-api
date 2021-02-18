from mcdashadmin.models import Employee, Shift, Shift_Detail
from .serializers import UserRegisterationSerializer, shift_detail_serializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from datetime import datetime as dt


# Create your views here.
@api_view(['POST',])
def registerNewUser(req):
    
    if req.method == 'POST':
        new_register_serializer = UserRegisterationSerializer(data=req.data)
        data = {}
        if new_register_serializer.is_valid():
            user = new_register_serializer.save()
            data['response'] = 'User registerd successfully'
            data['username'] = user.username
            data['token'] = Token.objects.get(user=user).key
        else:
            data = new_register_serializer.errors
        
        return Response(data)

@api_view(['GET',])
@authentication_classes([TokenAuthentication,])
def listUpcomingShifts(req):
    data = {}
    user = req.user
    if user is not None:
        # find the employee
        employee = Employee.objects.get(user=user)
        # get 7 upcoming shifts
        all_shifts = Shift.objects.filter(employee=employee, shift_detail__start_at__lte = dt.now())
        all_shifts_detail = []
        for shift in all_shifts:
            shift_detail = Shift_Detail.objects.get(shift=shift)
            all_shifts_detail.append(shift_detail)
        # create serializer
        serializer = shift_detail_serializer(all_shifts_detail, many=True)
        data['shifts'] = serializer.data
    return Response(data)
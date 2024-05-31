from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from vendor.serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from vendor.models import Vendor, PurchaseOrder, VendorPerformanceRecord
from vendor.serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceRecordSerializer
from rest_framework.permissions import IsAuthenticated
from vendor.serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth.models import User
from django.db.models import Avg, Count, F, ExpressionWrapper, fields
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404


class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        vendor_performance = get_object_or_404(VendorPerformanceRecord, vendor=vendor_id)
        serializer = VendorPerformanceRecordSerializer(vendor_performance)
        return Response(serializer.data)

    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        update_vendor_performance(purchase_order.vendor.id)
        return Response(status=status.HTTP_200_OK)


def update_vendor_performance(vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed_pos = completed_pos.count()
    if total_completed_pos > 0:
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count() / total_completed_pos
    else:
        on_time_delivery_rate = 0

    quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

    response_time_expression = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
    avg_response_time = completed_pos.annotate(response_time=response_time_expression).aggregate(avg_time=Avg('response_time'))['avg_time'] or timezone.timedelta()

    fulfillment_rate = PurchaseOrder.objects.filter(vendor=vendor).count() / PurchaseOrder.objects.filter(vendor=vendor, status='completed').count() if total_completed_pos > 0 else 0

    VendorPerformanceRecord.objects.update_or_create(
        vendor=vendor,
        defaults={
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time,
            'fulfillment_rate': fulfillment_rate
        }
    )

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration success'}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login success'}, status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email and Password not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        if pk:
            vendor = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'New Vendor Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Vendor data updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        return Response({'msg': 'Vendor Deleted'}, status=status.HTTP_200_OK)

class PurchaseOrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        vendor_id = request.query_params.get('vendor')
        if pk:
            purchaseorder = PurchaseOrder.objects.get(pk=pk)
            serializer = PurchaseOrderSerializer(purchaseorder)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'New Purchase Order Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        purchaseorder = PurchaseOrder.objects.get(pk=pk)
        serializer = PurchaseOrderSerializer(purchaseorder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Purchase Order data updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        purchaseorder = PurchaseOrder.objects.get(pk=pk)
        purchaseorder.delete()
        return Response({'msg': 'Purchase Order Deleted Successfully'}, status=status.HTTP_200_OK)
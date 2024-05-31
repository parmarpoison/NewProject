from rest_framework import serializers
from vendor.models import User
from .models import Vendor, PurchaseOrder, VendorPerformanceRecord


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2']
        extra_kwargs={
        'password':{'write_only':True}
        }
    
    def validate(self,attrs):
        password = attrs.get('password')
        rpassword = attrs.get('password2')
        if password != rpassword:
            raise serializers.ValidationError("password and confirm password does't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code',
                  'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time',
                  'fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date',
                  'items', 'quantity', 'status', 'quality_rating', 'issue_date',
                  'acknowledgment_date']


class VendorPerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformanceRecord
        fields = ['id', 'vendor', 'date', 'on_time_delivery_rate',
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
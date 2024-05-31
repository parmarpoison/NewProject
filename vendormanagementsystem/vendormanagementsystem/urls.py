from django.urls import path,include
from vendor import views

urlpatterns = [
    path('api/vendors/', views.VendorAPI.as_view(), name='vendor-list'),
    path('api/vendors/<int:pk>/', views.VendorAPI.as_view(), name='vendor-detail'),
    path('api/purchase_orders/', views.PurchaseOrderAPI.as_view(), name='purchase-order-list'),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderAPI.as_view(), name='purchase-order-detail'),
    path('api/register/',views.UserRegistrationView.as_view(),name='register'),
    path('api/login/',views.UserLoginView.as_view(),name='login'),
    path('api/vendors/<int:vendor_id>/performance/', views.VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.VendorPerformanceAPIView.as_view(), name='acknowledge_purchase_order'),
]


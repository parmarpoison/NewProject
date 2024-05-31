from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name,password=None,password2=None):
        """
        Creates and saves a User with the given email ,name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name=models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Vendor(models.Model):
    name = models.CharField(max_length=255, verbose_name="Vendor's name")
    contact_details = models.TextField(verbose_name="Contact information of the vendor")
    address = models.TextField(verbose_name="Physical address of the vendor")
    vendor_code = models.CharField(max_length=50, unique=True, verbose_name="A unique identifier for the vendor")
    on_time_delivery_rate = models.FloatField(verbose_name="Tracks the percentage of on-time deliveries")
    quality_rating_avg = models.FloatField(verbose_name="Average rating of quality based on purchase orders")
    average_response_time = models.FloatField(verbose_name="Average time taken to acknowledge purchase orders")
    fulfillment_rate = models.FloatField(verbose_name="Percentage of purchase orders fulfilled successfully")
    
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, verbose_name="Unique number identifying the PO")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Vendor")
    order_date = models.DateTimeField(verbose_name="Date when the order was placed")
    delivery_date = models.DateTimeField(verbose_name="Expected or actual delivery date of the order")
    items = models.TextField(verbose_name="Details of items ordered")  # Changed to TextField SQLite not supports jsonfield
    quantity = models.IntegerField(verbose_name="Total quantity of items in the PO")
    status = models.CharField(max_length=50, verbose_name="Current status of the PO")
    quality_rating = models.FloatField(null=True, blank=True, verbose_name="Rating given to the vendor for this PO")
    issue_date = models.DateTimeField(verbose_name="Timestamp when the PO was issued to the vendor")
    acknowledgment_date = models.DateTimeField(null=True, blank=True, verbose_name="Timestamp when the vendor acknowledged the PO")

class VendorPerformanceRecord(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Vendor")
    date = models.DateTimeField(verbose_name="Date of the performance record")
    on_time_delivery_rate = models.FloatField(verbose_name="Historical record of the on-time delivery rate")
    quality_rating_avg = models.FloatField(verbose_name="Historical record of the quality rating average")
    average_response_time = models.FloatField(verbose_name="Historical record of the average response time")
    fulfillment_rate = models.FloatField(verbose_name="Historical record of the fulfilment rate")

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
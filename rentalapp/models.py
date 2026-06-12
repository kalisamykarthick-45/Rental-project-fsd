from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bike(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    cc = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='bikes/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Laptop(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    processor = models.CharField(max_length=100)
    storage = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='laptops/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    megapixels = models.CharField(max_length=50)
    lens_type = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='cameras/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name  
    
     

PAYMENT_CHOICES = [
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Returned', 'Returned'),
    ('Completed', 'Completed'),
    ('Rejected', 'Rejected'),
]



class BikeBooking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey('Bike', on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    start_date = models.DateField()
    end_date = models.DateField()

    aadhar_card = models.ImageField(upload_to='bike_docs/aadhar/')
    driving_license = models.ImageField(upload_to='bike_docs/license/')
    selfie = models.ImageField(upload_to='bike_docs/selfie/')

    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    payment_proof = models.ImageField(upload_to='payments/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    late_fees = models.IntegerField(default=0)
    damage_charge = models.IntegerField(default=0, blank=True, null=True)

    returned_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    blank=True,
    null=True
)
    deposit_refunded = models.BooleanField(default=False)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        days = self.total_days
        rent = days * self.bike.price_per_day

        self.rent_amount = rent
        self.total_price = rent + self.security_deposit

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.bike.name}"

    





class LaptopBooking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey('Laptop', on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    start_date = models.DateField()
    end_date = models.DateField()

    aadhar_card = models.ImageField(upload_to='laptop_docs/aadhar/')
    driving_license = models.ImageField(upload_to='laptop_docs/license/')
    selfie = models.ImageField(upload_to='laptop_docs/selfie/')

    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    payment_proof = models.ImageField(upload_to='payments/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    late_fees = models.IntegerField(default=0)
    damage_charge = models.IntegerField(default=0, blank=True, null=True)

    returned_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    blank=True,
    null=True
)
    deposit_refunded = models.BooleanField(default=False)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        days = self.total_days
        rent = days * self.laptop.price_per_day

        self.rent_amount = rent
        self.total_price = rent + self.security_deposit

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.laptop.name}"






class CameraBooking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    start_date = models.DateField()
    end_date = models.DateField()

    aadhar_card = models.ImageField(upload_to='camera_docs/aadhar/')
    driving_license = models.ImageField(upload_to='camera_docs/license/')
    selfie = models.ImageField(upload_to='camera_docs/selfie/')

    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=2500)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    payment_proof = models.ImageField(upload_to='payments/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    late_fees = models.IntegerField(default=0)
    damage_charge = models.IntegerField(default=0, blank=True, null=True)

    returned_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    blank=True,
    null=True
)
    deposit_refunded = models.BooleanField(default=False)


    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        days = self.total_days
        rent = days * self.camera.price_per_day

        self.rent_amount = rent
        self.total_price = rent + self.security_deposit

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.camera.name}"
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
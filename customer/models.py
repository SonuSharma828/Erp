from django.db import models
from utils.geocode import get_coordinates_from_google

class Customer(models.Model):
    invoice = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    address = models.TextField()
    country_code = models.CharField(max_length=5, choices=[
        ('+91', '+91'),
        ('+1', '+1'),
        ('+44', '+44'),
        ('+61', '+61'),
    ], default='+91')
    phone = models.CharField(max_length=35)
    email = models.EmailField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.customer_name
    '''
    def save(self, *args, **kwargs):
        if (not self.latitude or not self.longitude) and self.address:
            lat, lng = geocode_address(self.address)
            if lat and lng:
                self.latitude = lat
                self.longitude = lng
        super().save(*args, **kwargs)
    '''
    '''
    def save(self, *args, **kwargs):
        if self.address and (self.latitude is None or self.longitude is None):
            # Call Google API here using your API key from settings
            api_key = settings.GOOGLE_MAPS_API_KEY
            lat, lng = get_coordinates_from_google(self.address, api_key)
            if lat and lng:
                self.latitude = lat
                self.longitude = lng
        super().save(*args, **kwargs)
    '''

class ContactPerson(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.phone})"

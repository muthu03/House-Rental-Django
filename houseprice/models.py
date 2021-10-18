from django.db import models, migrations


class renteeform(models. Model):
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=13)
    address = models.TextField(max_length=500)
    gender = models.CharField(max_length=15)
    bedrooms = models.CharField(max_length=10)
    bathrooms = models.CharField(max_length=11)
    image = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=100)

    def _str_(self):
        return self.first_name

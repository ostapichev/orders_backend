from django.db import models


class OrderModel(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    age = models.IntegerField()
    course = models.CharField(max_length=5)
    course_format = models.CharField(max_length=10)
    course_type = models.CharField(max_length=20)
    alreadyPaid = models.IntegerField()
    sum = models.IntegerField()
    msg = models.TextField(max_length=255)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    utm = models.CharField(max_length=35)

    class Meta:
        db_table = 'orders'




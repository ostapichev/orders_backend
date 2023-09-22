from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        db_table = 'profile'

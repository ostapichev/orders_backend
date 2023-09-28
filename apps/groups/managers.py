from django.db import models


class GroupManager(models.Manager):
    def all_with_orders(self):
        return self.prefetch_related('orders')

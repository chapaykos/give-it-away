from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Institution(models.Model):
    CHARITY_TYPE = (
        ('1', 'fundacja'),
        ('2', 'organizacja pozarządowa'),
        ('3', 'zbiórka lokalna')
    )
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=CHARITY_TYPE, default=1)
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.name

    def category_ids(self):
        return ', '.join([str(category.id) for category in self.categories.all()])


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    zip_code = models.CharField(max_length=256)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"Donation #{self.id} for '{self.institution}' by {self.user}"

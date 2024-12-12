from django.db import models


class NOOS(models.Model):
    itemCard = models.CharField(max_length=9)
    itemName = models.CharField(max_length=100)



#item itemCard -> Strilnr, nafn, verð, stærð + magn






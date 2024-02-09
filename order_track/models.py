from django.db import models
from main.models import Data

class Order(models.Model):

    AmazonOrderId = models.CharField(max_length=100 , null=True , blank=True )
    Tracknumber = models.CharField(max_length=200 , null=True , blank=True)
    Tracknumber2 = models.CharField(max_length=200 , null=True , blank=True)
    Courier_Name = models.CharField(max_length=200 , null=True , blank=True)
    Last_Status = models.CharField(max_length=500 , null=True , blank=True)
    Status = models.CharField(max_length=50 , null=True , blank=True)    

    def __str__(self):
        
        
        return self.AmazonOrderId + ' ' + str(self.Tracknumber or ' ') 


     
    
class OrderFileData(models.Model):
    file = models.FileField()


from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=255, unique=True)  
  symbol = models.CharField(max_length=10, unique=True, primary_key=True) 
  cash_flow = models.JSONField()  
  income_statement = models.JSONField() 
  balance_sheet = models.JSONField() 
  profitability = models.JSONField()  


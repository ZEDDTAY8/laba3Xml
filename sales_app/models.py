from django.db import models

class Sale(models.Model):
    product = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateField()
    # 

    class Meta:
        unique_together = ['product', 'price', 'quantity', 'date']  # Проверка дубликатов по комбинации полей

    def __str__(self):
        return f"{self.product} - {self.price}"
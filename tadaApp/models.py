from django.db import models

# IMPORTANT: models are created manually using the sql

# class TaDaRateSheet(models.Model):
#     grade = models.IntegerField()
#     daily_allowance = models.DecimalField(max_digits=10, decimal_places=2)

# class DistanceMatrix(models.Model):
#     oid = models.AutoField(primary_key=True)
#     distance_matrix_id = models.CharField(max_length=255)
#     start_location_id = models.CharField(max_length=255)
#     start_location_name_en = models.CharField(max_length=255)
#     start_location_name_bn = models.CharField(max_length=255)
#     end_location_id = models.CharField(max_length=255)
#     end_location_name_en = models.CharField(max_length=255)
#     end_location_name_bn = models.CharField(max_length=255)
#     distance = models.FloatField()
#     remarks = models.TextField()

    # def __str__(self):
    #     return f"{self.distance_matrix_id} - {self.start_location_name_en} to {self.end_location_name_en}"

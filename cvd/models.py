from django.db import models
from django.utils import timezone


# class cvd(models.Model):
#     time_choices = (
#         ('morning', "Morning"),
#         ('evening', "Evening")
#     )
#     name = models.CharField(max_length=120)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     doctor = models.ForeignKey(
#         Doctor, on_delete=models.CASCADE, related_name='cvd')
#     date = models.DateField(default=timezone.now)
#     time = models.CharField(choices=time_choices, max_length=10)
#     note = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name}-{self.doctor.name}"

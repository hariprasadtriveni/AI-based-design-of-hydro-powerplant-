from django.db import models

# Create your models here.
from django.db import models

class HydroPowerDesign(models.Model):
    location = models.CharField(max_length=255)
    river_flow = models.FloatField()
    budget = models.FloatField()
    power_requirement = models.FloatField()
    civil_design_text = models.TextField(null=True, blank=True)
    civil_design_image = models.URLField(null=True, blank=True)
    hydroelectric_text = models.TextField(null=True, blank=True)
    hydroelectric_image = models.URLField(null=True, blank=True)
    mechanical_text = models.TextField(null=True, blank=True)
    mechanical_image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Design for {self.location}"


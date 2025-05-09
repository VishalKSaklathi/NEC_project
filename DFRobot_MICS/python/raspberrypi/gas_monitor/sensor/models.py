from django.db import models
#x
class GasReading(models.Model):
    timestamp = models.DateTimeField()

    humidity = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    CO = models.FloatField(default=0.0)
    NO2 = models.FloatField(default=0.0)
    NH3 = models.FloatField(default=0.0)
    H2 = models.FloatField(default=0.0)
    CH4 = models.FloatField(default=0.0)
    C2H5OH = models.FloatField(default=0.0)


    def __str__(self):
        return f"Gas reading at (self.timestamp)"
#x

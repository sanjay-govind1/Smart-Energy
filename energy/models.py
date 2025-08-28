from django.db import models

class EnergyReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device_name = models.CharField(max_length=100)
    current_power = models.FloatField()  
    today_energy = models.FloatField()   
    month_energy = models.FloatField()
    runtime_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.device_name} - {self.current_power}W at {self.timestamp}"


class SensorReading(models.Model):
    temperature = models.FloatField()
    ldr = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature} °C, LDR {self.ldr}"

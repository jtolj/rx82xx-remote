from django.db import models
from django.conf import settings

# Create your models here.

class Schedule_event(models.Model):
    datetime = models.DateTimeField('start time')
    receiver = models.CharField(choices = zip(settings.RECEIVERS.keys(), settings.RECEIVERS.keys()),max_length=200)
    schedule = models.CharField(choices = zip(settings.SCHEDULES.keys(), settings.SCHEDULES.keys()),max_length=200)
    status = models.IntegerField(default=0)

    def statustext(self):
        output = ["To Be Scheduled", "Scheduled", "Pending Update", "Deleted", "Error", "Completed"]
        return output[self.status]
    
    def statusclass(self):
        if (self.status == 0 or self.status == 2):
            return 'warning'
        elif (self.status == 1 or self.status == 5):
            return 'ok'
        elif (self.status == 3 or self.status == 4):
            return 'error'
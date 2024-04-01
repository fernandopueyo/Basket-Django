from django.db import models
from calendar_basket.models import User, Teams

class Players(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_team = models.ForeignKey(Teams, models.CASCADE, db_column='id_team')
    dorsal = models.BigIntegerField(null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'players'

    def is_complete(self):
        if self.first_name and self.id_team:
            return True
        else:
            return False
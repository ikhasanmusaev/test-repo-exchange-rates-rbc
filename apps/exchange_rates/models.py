from django.db import models


class Currency(models.Model):
    id_cbr = models.CharField(max_length=10, verbose_name='ID_CBR', unique=True)
    num_code = models.CharField(max_length=5, verbose_name='cbr_num_code', unique=True)
    char_code = models.CharField(max_length=5, verbose_name='cbr_char_code')
    name = models.CharField(max_length=100, verbose_name='Currency name')

    @property
    def last_rate_of_currency(self):
        if self.daily_rate.all().exists():
            return self.daily_rate.all().first()
        return None


class DailyRate(models.Model):
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, related_name='daily_rate')
    nominal = models.IntegerField(verbose_name='Nominal', default=1)
    value = models.FloatField()
    date = models.DateField()

    class Meta:
        ordering = ['-date']


class UserCurrency(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
    threshold = models.FloatField(default=1)

    class Meta:
        unique_together = ('user', 'currency',)

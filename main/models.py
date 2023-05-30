from django.db import models
import datetime as dt
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
from django.utils import timezone


def validate_half_hour(value):
    if isinstance(value, time):
        if value.minute not in [0, 30]:
            raise ValidationError('Laikam jābūt ar 30 minūšu soli.')


def validate_future_time(value):
    now = timezone.localtime()
    if isinstance(value, time):
        current_datetime = datetime.combine(now.date(), now.time())
        selected_datetime = datetime.combine(now.date(), value)

        current_datetime_plus_24h = current_datetime + timedelta(hours=24)

        if selected_datetime < current_datetime and selected_datetime >= current_datetime_plus_24h:
            raise ValidationError('Laikam nevajadzētu būt pagātnē.')

def validate_end_time_after_start_time(work_time1, work_time2):
    if work_time2 <= work_time1:
        raise ValidationError('Beigu laikam ir jābūt pēc sākuma laika.')


def validate_no_conflicting_tasks(works):
    # Izveidojam vārdnīcu, lai izsekotu, kuri laiki jau ir aizņemti
    taken_times = {}

    for work in works:
        work_time1 = work.work_time1
        work_time2 = work.work_time2

        # Pārbaudam, vai šis darbs nepārklājas ar kādu iepriekš ieplānotu darbu
        for taken_work_time1, taken_work_time2 in taken_times.values():
            if work_time1 < taken_work_time2 and work_time2 > taken_work_time1:
                # Ja darbs pārklājas ar citu uzdevumu, parādam validācijas kļūdu
                raise ValidationError('Darbu laiki nedrīkst pārklāties.')

        # Pievienojam darba sākuma un beigu laikus take_times vārdnīcai
        taken_times[work.id] = (work_time1, work_time2)



class Work(models.Model):
    work_name = models.CharField(max_length=20, verbose_name='Darba nosaukums')
    work_date = models.DateField(verbose_name='Darba diena')
    work_time1 = models.TimeField(validators=[validate_half_hour, validate_future_time], verbose_name='Sākums')
    work_time2 = models.TimeField(validators=[validate_half_hour, validate_future_time], verbose_name='Beigas')

    def clean(self):
        validate_end_time_after_start_time(self.work_time1, self.work_time2)

        if self.id is not None:
            works = Work.objects.exclude(id=self.id)
            works = works.filter(work_time1__lte=self.work_time2, work_time2__gte=self.work_time1)
            validate_no_conflicting_tasks(works)

    def __str__(self):
        return self.work_name


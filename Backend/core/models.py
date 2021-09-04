from datetime import timedelta

from django.db import models
from user.models import User


def emi_calculator(p, r, t):
    # emi = P × r × (1 + r)n/((1 + r)n - 1)
    r = r / (12 * 100)
    # t = t * 12
    emi = (p * r * pow(1 + r, t)) / (pow(1 + r, t) - 1)
    return round(emi, 2)


class Loan(models.Model):
    amount = models.BigIntegerField()
    interest_rate = models.FloatField(verbose_name='Rate of interest')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='duration in month(s)'
    )

    status_choice = (
        ('new', 'NEW'),
        ('rejected', 'REJECTED'),
        ('approved', 'APPROVED'),
    )
    status = models.CharField(
        max_length=50,
        choices=status_choice,
        default='new'
    )

    emi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='EMI per month(s)'
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='user_agent',
        null=True
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='user_customer',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self):
        return super(Loan, self).__str__()

     # emi = P × r × (1 + r)n/((1 + r)n - 1)
    def calculate_emi(self):
        if self.duration != None and self.interest_rate != None:
            emi = emi_calculator(
                self.amount,
                self.interest_rate,
                self.duration
            )
            return emi
        return None

    def save(self, *args, **kwargs):
        self.emi = self.calculate_emi()
        if self.start_date and self.duration:
            self.end_date = self.start_date+timedelta(days=self.duration*30)
        super(Loan, self).save(*args, **kwargs)

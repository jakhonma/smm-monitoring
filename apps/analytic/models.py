from django.db import models
from apps.employee.models import SMMStaff
from apps.channel.models import ChannelSocialAccount, SocialNetwork
from .validators import validate_year, validate_month, validate_not_future_year_month
from django.core.exceptions import ValidationError


class ChannelSocialStats(models.Model):
    """Har oy uchun statistik ma’lumotlar"""
    smm_staff = models.ForeignKey(
        to=SMMStaff, 
        on_delete=models.CASCADE, 
        related_name='monthly_stats'
    )
    channel_social_account = models.ForeignKey(
        to=ChannelSocialAccount,
        on_delete=models.SET_NULL,
        editable=True,
        null=True,
        blank=True
    )
    year = models.PositiveIntegerField(validators=[validate_year])
    month = models.PositiveIntegerField(validators=[validate_month])
    views = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    content_count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['smm_staff', 'year', 'month'],
                name='unique_staff_year_month'
            )
        ]
        ordering = ['-year', '-month']
    
    def clean(self):
        validate_not_future_year_month(self.year, self.month)
        return super().clean()
    
    def save(self, *args, **kwargs):
        # smm_staff orqali channel_social_account avtomatik set qilinadi
        if self.smm_staff and not self.channel_social_account:
            self.channel_social_account = self.smm_staff.channel_social_account
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.smm_staff} → {self.year}-{self.month}"


class KPIFormula(models.Model):
    SOCIAL_METRICS = [
        ("content", "Content count"),
        ("views", "Views"),
        ("followers", "Followers"),
    ]
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    metric = models.CharField(max_length=30, choices=SOCIAL_METRICS)
    min_value = models.PositiveIntegerField()    # shu qiymatga yetganda ball olinadi
    points = models.PositiveIntegerField()          # shu min_value uchun beriladigan ball

    class Meta:
        ordering = ["-min_value"]  # adminda ustun tartib uchun
    
    def __str__(self):
        return f"{self.social_network} - {self.metric} -> {self.min_value} -> {self.points}"

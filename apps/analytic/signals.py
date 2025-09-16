from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.analytic.models import KPIFormula
from apps.analytic.kpi_formula_cache import RedisKPICache


@receiver(post_save, sender=KPIFormula)
@receiver(post_delete, sender=KPIFormula)
def update_kpi_cache(sender, **kwargs):
    """KPIFormula o‘zgarganda cache yangilanadi"""
    RedisKPICache().refresh()

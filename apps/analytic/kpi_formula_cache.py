from abc import ABC, abstractmethod
from django.core.cache import cache
from .models import KPIFormula
from collections import defaultdict

KPI_CACHE_KEY = "kpi_formula_cache"


class IKPICache(ABC):
    """KPI cache interfeysi (Abstraction - DIP)"""

    @abstractmethod
    def refresh(self) -> None:
        pass

    @abstractmethod
    def get_data(self) -> dict:
        pass


class RedisKPICache(IKPICache):
    """Redis orqali KPI cache (SRP - faqat cache ishlash uchun mas’ul)"""

    def refresh(self) -> None:
        formulas = KPIFormula.objects.select_related("social_network").all()

        grouped = defaultdict(lambda: defaultdict(list))
        for f in formulas:
            grouped[f.social_network.name][f.metric].append(
                {
                    # "id": f.id,
                    "min_value": f.min_value,
                    "points": f.points,
                }
            )

        # Har bir metric ichida min_value bo‘yicha sortlab qo‘yamiz
        for sn_name, metrics in grouped.items():
            for metric, rows in metrics.items():
                rows.sort(key=lambda x: x["min_value"])

        cache.set(KPI_CACHE_KEY, dict(grouped), timeout=None)

    def get_data(self) -> dict:
        data = cache.get(KPI_CACHE_KEY)
        if not data:
            self.refresh()
            data = cache.get(KPI_CACHE_KEY)
        return data

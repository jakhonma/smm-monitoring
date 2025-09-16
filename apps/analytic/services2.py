from collections import defaultdict
from .models import KPIFormula


class KPIFormulaCache:
    """
    KPI formulalarini DB dan bitta marta olib, 
    ijtimoiy tarmoq va metrik bo‘yicha tezkor qidiruvga tayyorlab beradi.
    """

    def __init__(self):
        self.formula_map = self._load_formulas()

    def _load_formulas(self):
        formulas = KPIFormula.objects.select_related("social_network").all()
        formula_map = defaultdict(lambda: defaultdict(list))

        for f in formulas:
            formula_map[f.social_network.name][f.metric].append((f.min_value, f.points))

        # Har bir metrik uchun min_value ni kamayish tartibida sort qilish
        for sn, metrics in formula_map.items():
            for metric, rules in metrics.items():
                formula_map[sn][metric] = sorted(rules, key=lambda x: -x[0])

        return formula_map

    def get_points(self, social_network: str, metric: str, value: int) -> int:
        rules = self.formula_map.get(social_network, {}).get(metric, [])
        for min_value, points in rules:
            if value >= min_value:
                return points
        return 0


# Init (bir marta chaqiriladi, masalan service layerda yoki startup da)
# kpi_cache = KPIFormulaCache()

# # Xodimning Instagram content ballini olish
# points = kpi_cache.get_points("Instagram", "content", 95)
# print(points)  # jadvalga qarab ball chiqadi

# # Views uchun ham xuddi shunday
# points = kpi_cache.get_points("Instagram", "views", 50000)

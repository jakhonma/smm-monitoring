from abc import ABC, abstractmethod

from .kpi_formula_cache import IKPICache
# from .services import KPIService


class NetworkScore(ABC):
    def __init__(self, services, cache: IKPICache, network_name: str):
        self.cache = cache
        self.network_name = network_name
        self.services = services

    def score_count(self, value, social_type):
        rules = self.cache.get_data()
        network_rules = rules.get(self.network_name, {})
        metric_rules = network_rules.get(social_type, [])
        min_value = 0
        # print(social_type, value, metric_rules)
        for rule in metric_rules:
            if rule["min_value"] < value:
                min_value = rule["points"]
                break
        return min_value


class Instagram(NetworkScore):
    def __init__(self, services,  cache):
        super().__init__(services, cache, "Instagram")


class Telegram(NetworkScore):
    def __init__(self, services, cache):
        super().__init__(services, cache, "Telegram")


class Facebook(NetworkScore):
    def __init__(self, services, cache):
        super().__init__(services, cache, "Facebook")

from .models import KPIFormula, KPIThreshold
from abc import ABC, abstractmethod


def kpi_percent(score: int) -> str:
    ranges = (
        ((95, 100), 100),
        ((89, 94), 90),
        ((84, 88), 80),
        ((78, 83), 70),
        ((72, 77), 60),
        ((66, 71), 50),
        ((60, 65), 40),
        ((54, 59), 30),
        ((48, 53), 20),
        ((42, 47), 10),
    )
    for (low, high), percent in ranges:
        if low <= score <= high:
            return percent
    return 0  # agar past bo'lsa


class NetworkScore(ABC):
    @abstractmethod
    def score_count(self, value, social_type):
        pass


class Instagram(NetworkScore):
    def score_count(self, value, social_type):
        return super().score_count(value, social_type)


class Telegram(NetworkScore):
    def score_count(self, value, social_type):
        return super().score_count(value, social_type)


class Facebook(NetworkScore):
    def score_count(self, value, social_type):
        return super().score_count(value, social_type)


class KPIService:
    def __init__(self, data):
        self.data = data
        self.employee = []
        self.instagram = 'instagram'
        self.telegram = 'telegram'
        self.facebook = 'facebook'
    
    def content_score(value):
        pass

    def views_score(value):
        pass

    def followers_score(value):
        pass

from .kpi_formula_cache import IKPICache
from .network_score import Instagram, Telegram, Facebook

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


class KPIService:
    def __init__(self, data, cache: IKPICache):
        self.data = data
        self.cache = cache

        # Cache’dan oladigan network handlerlar
        self.networks = {
            "instagram": Instagram(self, cache),
            "telegram": Telegram(self, cache),
            "facebook": Facebook(self, cache),
        }

    @staticmethod
    def get_points(value, rules):
        for rule in rules:
            if value >= rule["min_value"]:
                return rule["points"]
        return 0

    @staticmethod
    def calc_percentage(prev, current):
        if prev == 0:
            return 100 if current > 0 else 0
        return ((current - prev) / prev) * 100
    
    @staticmethod
    def calc_percentage2(prev, current):
        if prev == 0:
            return 100 if current > 0 else 0
        return (current / prev) * 100

    def evaluate(self):
        results = []
        for emp in self.data:
            emp_result = {"employee": emp["employee"], "channels": {}}

            for channel_name, networks in emp["channels"].items():
                channel_result = []
                for net in networks:
                    net_name = net["network"].lower()
                    current = net["current"]
                    prev = net["prev"]

                    handler = self.networks.get(net_name)
                    if not handler:
                        continue

                    percentages = {
                        m: self.calc_percentage(prev[m], current[m])
                        for m in ["views", "followers", "content"]
                    }

                    scores = {
                        m: handler.score_count(current[m], m)
                        for m in ["views", "followers", "content"]
                    }

                    channel_result.append({
                        "network": net["network"],
                        "percentages": percentages,
                        "scores": scores,
                        "total_score": sum(scores.values())
                    })

                emp_result["channels"][channel_name] = channel_result
            results.append(emp_result)
        employees = []
        for emp in self.data:
            total_score = 0
            employee_result = {"emp": emp["employee"], "channels": [], 'kpi': 0}
            for channel_name, networks in emp["channels"].items():
                score_sum = 0
                for net in networks:
                    net_name = net["network"].lower()
                    current = net["current"]
                    prev = net["prev"]

                    handler = self.networks.get(net_name)
                    if not handler:
                        continue

                    view_percentage = self.calc_percentage2(prev["views"], current["views"])
                    follower_percentage = self.calc_percentage2(prev["followers"], current["followers"])
                    view_score = handler.score_count(view_percentage, "views")
                    follower_score = handler.score_count(follower_percentage, "followers")
                    content_score = handler.score_count(current["content"], "content")
                    score_sum += view_score + follower_score + content_score
                    print(view_score, follower_score, content_score)
                    print(score_sum, 333333333)
                total_score += score_sum
                employee_result["channels"].append({
                    "channel": channel_name,
                    "score": score_sum
                })
            kpi_result = kpi_percent(total_score)
            employee_result["kpi"] = kpi_result
            employees.append(employee_result)
        return employees


from django.db.models import OuterRef, Subquery, IntegerField, Value, Sum
from django.db.models.functions import Coalesce
import datetime
from apps.employee.models import Employee
from .models import ChannelSocialStats

# def employee_data():
#     today = datetime.date.today()
#     this_year, this_month = today.year, today.month

#     # Oldingi oy hisoblash
#     if this_month == 1:
#         prev_year, prev_month = this_year - 1, 12
#     else:
#         prev_year, prev_month = this_year, this_month - 1

#     stats_qs = ChannelSocialStats.objects.filter(
#         smm_staff__employee=OuterRef("pk"),
#         year=this_year,
#         month=this_month
#     )
#     prev_stats_qs = ChannelSocialStats.objects.filter(
#         smm_staff__employee=OuterRef("pk"),
#         year=prev_year,
#         month=prev_month
#     )

#     employees = Employee.objects.annotate(
#         current_views=Coalesce(Subquery(stats_qs.values("views")[:1]), Value(0)),
#         current_followers=Coalesce(Subquery(stats_qs.values("followers")[:1]), Value(0)),
#         current_content=Coalesce(Subquery(stats_qs.values("content_count")[:1]), Value(0)),

#         prev_views=Coalesce(Subquery(prev_stats_qs.values("views")[:1]), Value(0)),
#         prev_followers=Coalesce(Subquery(prev_stats_qs.values("followers")[:1]), Value(0)),
#         prev_content=Coalesce(Subquery(prev_stats_qs.values("content_count")[:1]), Value(0)),
#     )
#     return employees

from collections import defaultdict
import datetime


def employee_data():
    today = datetime.date.today()
    this_year, this_month = today.year, today.month

    # Oldingi oy hisoblash
    if this_month == 1:
        prev_year, prev_month = this_year - 1, 12
    else:
        prev_year, prev_month = this_year, this_month - 1

    # Joriy oy stats
    this_stats = ChannelSocialStats.objects.filter(
        year=this_year, month=this_month
    ).values(
        "smm_staff__employee_id",
        "smm_staff__employee__first_name",
        "smm_staff__employee__last_name",
        "channel_social_account__channel__name",   # <-- Kanal nomi
        "channel_social_account__social_network__name"
    ).annotate(
        views=Sum("views"),
        followers=Sum("followers"),
        content_count=Sum("content_count"),
    )

    # Oldingi oy stats
    prev_stats = ChannelSocialStats.objects.filter(
        year=prev_year, month=prev_month
    ).values(
        "smm_staff__employee_id",
        "smm_staff__employee__first_name",
        "smm_staff__employee__last_name",
        "channel_social_account__channel__name",   # <-- Kanal nomi
        "channel_social_account__social_network__name"
    ).annotate(
        views=Sum("views"),
        followers=Sum("followers"),
        content_count=Sum("content_count"),
    )

    # Dictionaryga yig‘ish
    employees_data = defaultdict(lambda: {"employee": None, "channels": defaultdict(list)})

    for row in this_stats:
        emp_id = row["smm_staff__employee_id"]
        employees_data[emp_id]["employee"] = f"{row['smm_staff__employee__first_name']} {row['smm_staff__employee__last_name']}"
        channel = row["channel_social_account__channel__name"]
        employees_data[emp_id]["channels"][channel].append({
            "network": row["channel_social_account__social_network__name"],
            "current": {
                "views": row["views"],
                "followers": row["followers"],
                "content": row["content_count"],
            },
            "prev": {"views": 0, "followers": 0, "content": 0}  # default
        })

    for row in prev_stats:
        emp_id = row["smm_staff__employee_id"]
        channel = row["channel_social_account__channel__name"]
        for sn in employees_data[emp_id]["channels"][channel]:
            if sn["network"] == row["channel_social_account__social_network__name"]:
                sn["prev"] = {
                    "views": row["views"],
                    "followers": row["followers"],
                    "content": row["content_count"],
                }
    return employees_data

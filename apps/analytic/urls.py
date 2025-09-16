from django.urls import path
from .views import ChannelWithStatsView, EmployeeKPIView

urlpatterns = [
    path('channel/<int:pk>/', ChannelWithStatsView.as_view(), name='channel-stats'),
    path('employee-kpi/', EmployeeKPIView.as_view(), name="employye-kpi"),
]
from rest_framework import generics, views, response
from apps.analytic.serializers import EmployeeKPISerializer
from apps.employee.models import Employee
from apps.analytic.query import employee_data
from apps.analytic.kpi_formula_cache import RedisKPICache


# class EmployeeKPIView(generics.ListAPIView):
#     serializer_class = EmployeeKPISerializer

#     def get_queryset(self):
#         employee = Employee.objects.all()
#         return employee


class EmployeeKPIView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        data = employee_data().values()
        data = RedisKPICache().get_data()
        return response.Response(data=data)

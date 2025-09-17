from rest_framework import generics, views, response
from apps.analytic.serializers import EmployeeKPISerializer
from apps.analytic.services import KPIService
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
        # data = RedisKPICache().get_data()

        kpi_cache = RedisKPICache()

        service = KPIService(data, kpi_cache)
        result = service.evaluate()
        return response.Response(data=result)

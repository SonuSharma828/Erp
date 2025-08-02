from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TechnicianLoginSerializer,TaskListSerializer,TaskListSerializer,TaskStatusUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from manage_tasks.models import Task
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import UpdateAPIView
from employees.models import Employee
from rest_framework import permissions
from .serializers import ProfileUpdateSerializer
from core.models import TransactionType
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from dashboard.models import CustomUser 
from STK.models import STKTake
from .serializers import STKTakeSerializer,TaskBillingSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from STK.models import STKTake, STKStock
from .serializers import STKTakeCreateSerializer
from django.utils.timezone import now

from rest_framework.generics import ListAPIView
from core.models import PaymentMode
from .serializers import PaymentModeSerializer

class PaymentModeListView(ListAPIView):
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        request = self.context.get('request')

        # Try to get related Employee object like in your profile API
        employee = None
        try:
            from employees.models import Employee  # adjust import as needed
            employee = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            pass

        # Build photo URL either from user.photo or employee.photo
        photo_url = None
        if employee and employee.photo:
            photo_url = request.build_absolute_uri(employee.photo.url) if request else employee.photo.url
        elif hasattr(user, 'photo') and user.photo:
            photo_url = request.build_absolute_uri(user.photo.url) if request else user.photo.url

        data.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'department': user.department.department_name if hasattr(user, 'department') and user.department else None,
            'photo': photo_url,
        })
        return data


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get all refresh tokens for this user
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                try:
                    RefreshToken(token.token).blacklist()
                except TokenError:
                    pass
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# api/views.py
from rest_framework.viewsets import ModelViewSet
from manage_tasks.models import ServiceCharge,CoWorkerCharge
from .serializers import ServiceChargeSerializer
from rest_framework.permissions import IsAuthenticated

class ServiceChargeViewSet(ModelViewSet):
    queryset = ServiceCharge.objects.all()
    serializer_class = ServiceChargeSerializer
    permission_classes = [IsAuthenticated]


# for test token
class TokenTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"success": True, "user": request.user.username})


from manage_tasks.models import ManualItem,ExternalExpense
class TaskBillingCreateView(APIView):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        # Inject task into billing data before validation
        billing_data = request.data.copy()
        billing_data['task'] = task.sno  # assuming task.sno is primary key


        # Inject technician
        if hasattr(request.user, 'employee') and request.user.employee:
            billing_data['technician'] = request.user.employee.sno
        else:
            return Response({'technician': 'No linked employee found for user.'}, status=400)
        if hasattr(task, 'billing'):
            return Response({"task": ["Task billing with this task already exists."]}, status=400)
        serializer = TaskBillingSerializer(data=billing_data, context={'request': request})

        if serializer.is_valid():
            billing = serializer.save()

            # Save manual items
            manual_items = request.data.get('manual_items', [])
            for item in manual_items:
                ManualItem.objects.create(
                    task=task,
                    item_name=item.get('item_name'),
                    note=item.get('note', ''),
                    quantity=item.get('quantity', 1),
                    price=item.get('price', 0),
                )

            # Save external expenses
            expenses = request.data.get('expenses', [])
            for expense in expenses:
                ExternalExpense.objects.create(
                    task=task,
                    item_name=expense.get('item_name'),
                    note=expense.get('note', ''),
                    quantity=expense.get('quantity', 1),
                    price=expense.get('price', 0),
                )
            # Optional co-worker charges
            coworkers = request.data.get('coworkers', [])
            for coworker in coworkers:
                CoWorkerCharge.objects.create(
                task=task,
                charge=coworker.get('charge', 0),
                )


            # Calculate totals
            manual_total = sum(item['quantity'] * item['price'] for item in manual_items)
            expense_total = sum(exp['quantity'] * exp['price'] for exp in expenses)
            coworker_total = sum(c['charge'] for c in coworkers if 'charge' in c)
            tools_total = float(request.data.get('tools_total', 0))
            service_total = float(request.data.get('service_total', 0))
            final_total = tools_total + service_total + manual_total + expense_total + coworker_total

            # Save final total
            billing.final_total = final_total
            billing.save(update_fields=['final_total'])
            task.status = 'completed'
            task.save(update_fields=['status'])

            return Response(TaskBillingSerializer(billing).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#profile view
class TechnicianProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            employee = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            employee = None

        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'department': user.department.department_name if user.department else None,
            'employee': {
                'name': employee.name if employee else None,
                'position': employee.position if employee else None,
                'phone': employee.phone if employee else None,
                'address': employee.address if employee else None,
                'joining_date': employee.joining_date if employee else None,
                'salary': str(employee.salary) if employee else None,
                'photo': request.build_absolute_uri(employee.photo.url) if employee and employee.photo else None,
            } if employee else None
        })
'''
# Technician Task List View
class TechnicianTaskListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user).order_by('date')
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)
'''
class TechnicianTaskListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = request.user.employee
        if not employee:
            return Response({"detail": "No Employee profile linked with this user."}, status=404)

        tasks = Task.objects.filter(assigned_to=employee).order_by('date')
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

# Technician Task Detail View
class TechnicianTaskDetailView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self):
        # Only return tasks assigned to the currently authenticated technician
        return Task.objects.filter(assigned_to=self.request.user)

class TaskStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(sno=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        allowed_statuses = ['accepted', 'rejected', 'waiting']

        if new_status not in allowed_statuses:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == 'accepted':
            task.status = 'in_progress'
        else:
            task.status = new_status
        task.save()
        return Response({"detail": "Status updated", "status": task.status}, status=status.HTTP_200_OK)

class TechnicianProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompletedTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user, status='completed').order_by('-date')



'''
class FilteredTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)
        qs = Task.objects.filter(assigned_to=user)
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-date')
'''

class FilteredTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.employee:
            return Task.objects.none()  # return empty queryset safely

        status = self.request.query_params.get('status', None)
        qs = Task.objects.filter(assigned_to=user.employee)

        if status:
            qs = qs.filter(status=status)

        return qs.order_by('-date')

class IssuedItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        items = STKTake.objects.filter(taken_by=user, transaction_type__name__iexact='out').order_by('-date')
        serializer = STKTakeSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


class ReturnItemView(CreateAPIView):
    serializer_class = STKTakeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        data = serializer.validated_data
        stock_item = data['item']
        return_qty = data['quantity']

        # Increase stock quantity
        stock_item.quantity += return_qty
        stock_item.save()

        # Assign transaction type = "IN"
        in_type = TransactionType.objects.get(name__iexact='in')

        # Save the transaction with extra fields
        serializer.save(taken_by=user, transaction_type=in_type, date=now())

        # ✅ Custom response
        return Response(
            {
                "message": f"{return_qty} units of {stock_item.item_name} returned successfully."
            },
            status=status.HTTP_201_CREATED
        )




from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from manage_tasks.models import Task
from utils.location import haversine_distance

class StartTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(sno=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        # Validate location input
        try:
            lat = float(request.data.get("latitude"))
            lng = float(request.data.get("longitude"))
        except (TypeError, ValueError):
            return Response({"detail": "Invalid or missing coordinates."}, status=status.HTTP_400_BAD_REQUEST)

        customer = task.customer
        if not customer.latitude or not customer.longitude:
            return Response({"detail": "Customer location not available."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate distance
        distance = haversine_distance(lat, lng, customer.latitude, customer.longitude)
        if distance > 100:
            return Response({
                "detail": "You are too far from customer location.",
                "distance_meters": int(distance)
            }, status=status.HTTP_403_FORBIDDEN)

        # Update task status
        task.status = 'started'  
        task.save()

        return Response({
            "detail": "Task started successfully.",
            "distance_meters": int(distance)
        }, status=status.HTTP_200_OK)


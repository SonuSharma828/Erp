from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from HRM.models import Department
from dashboard.models import CustomUser
from employees.models import Employee
from STK.models import STKTake
from rest_framework import serializers
from manage_tasks.models import ServiceCharge
from manage_tasks.models import Task,ExternalExpense,ManualItem

from rest_framework import serializers
from core.models import PaymentMode

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = ['id', 'name']  # Add any other fields if needed


class ServiceChargeSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCharge
        fields = ['id', 'name', 'charge', 'tax_percent', 'total_price']

    def get_total_price(self, obj):
        return obj.total_with_tax()

    def get_service_charges(self, obj):
        charges = ServiceCharge.objects.all()
        return ServiceChargeSerializer(charges, many=True).data

class TechnicianLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError(_('Invalid login credentials.'), code='authorization')

            if not user.department or user.department.department_name.lower() != 'technician':
                raise serializers.ValidationError(_('You are not authorized to use the app.'), code='authorization')

            attrs['user'] = user
            return attrs

        raise serializers.ValidationError(_('Must include "username" and "password".'), code='authorization')



from rest_framework import serializers
from manage_tasks.models import TaskBilling

class TaskBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBilling
        fields = ['task', 'tools_total', 'service_total', 'technician','final_total', 'payment_mode']
        read_only_fields = ['final_total']

'''
    def create(self, validated_data):
        tools_total = validated_data.get('tools_total', 0)
        service_total = validated_data.get('service_total', 0)

        # Get task instance
        task = validated_data.get('task')

        # ✅ Calculate manual_items total
        manual_items_total = sum([
            item.quantity * item.price for item in task.manual_items.all()])

        # ✅ Calculate expenses total
        expenses_total = sum([
            item.quantity * item.price for item in task.expenses.all()])

        # ✅ Calculate final total
        validated_data['final_total'] = tools_total + service_total + manual_items_total + expenses_total

        # Assign technician from user
        request = self.context.get('request')
        if request and hasattr(request.user, 'employee') and request.user.employee:
            validated_data['technician'] = request.user.employee
        else:
            raise serializers.ValidationError({'technician': 'No linked employee found for user.'})

        # Save the billing record
        billing = super().create(validated_data)

        # ✅ Mark task completed
        task.status = 'completed'
        task.save(update_fields=['status'])
        return billing

'''


class TaskListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
    customer_phone = serializers.SerializerMethodField()
    service = ServiceChargeSerializer(read_only=True)
    class Meta:
        model = Task
        fields = [
            'sno', 'task_detail', 'priority', 'location',
            'date', 'status',
            'customer_name', 'customer_phone','service',
        ]
        depth = 1  # So project and task_group names are included

    def get_customer_phone(self, obj):
        if obj.customer:
            return f"{obj.customer.country_code}-{obj.customer.phone}"
        return None

'''
class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Task._meta.get_field('status').choices]
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value



class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected', 'waiting']:
            raise serializers.ValidationError("Invalid status.")
        return value
'''

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected', 'waiting']:
            raise serializers.ValidationError("Invalid status.")
        return value
class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        # Update CustomUser fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update Employee fields
        try:
            employee = Employee.objects.get(email=instance.email)
        except Employee.DoesNotExist:
            employee = None

        if employee:
            employee.phone = validated_data.get('phone', employee.phone)
            employee.address = validated_data.get('address', employee.address)
            if 'photo' in validated_data:
                employee.photo = validated_data['photo']
            employee.save()

        return instance


from rest_framework import serializers
from STK.models import STKTake

class STKTakeSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    unit = serializers.CharField(source='item.unit.unit_name', read_only=True)
    category = serializers.CharField(source='item.category.category_name', read_only=True)
    transaction_type = serializers.StringRelatedField()
    class Meta:
        model = STKTake
        fields = ['id', 'item_name', 'category', 'unit', 'quantity', 'price', 'note', 'date', 'transaction_type']

class STKTakeCreateSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = STKTake
        fields = ['item', 'quantity', 'price', 'note','transaction_type']




class ManualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualItem
        fields = ['id', 'item_name', 'note', 'quantity', 'price']


class ExternalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalExpense
        fields = ['id', 'item_name', 'note', 'quantity', 'price']

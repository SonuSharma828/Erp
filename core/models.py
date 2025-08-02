from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class AmountType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TaskImportance(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ProjectType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ProjectStatus(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TaskStatus(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class PhotoIdType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Segment(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class PaymentMode(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class EntryType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ExpenseType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class VoucherType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class EmployeePaymentType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SppTransactionType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class AttendanceStatusType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class KnwGroupType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class KnwSubGroupType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

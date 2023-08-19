from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from app.users.doctor.models import Doctor, Review, Appointment, Package
from app.users.patient.models import Patient
# from app.users.models import Address

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Wallet(models.Model):
    """
    Wallet model manages the monetary balance for a user, tracking available funds.
    """
    walletId = models.AutoField(primary_key=True)
    balance = models.FloatField()

    # One Wallet can belong to either a Doctor or a Patient
    doctor = models.OneToOneField(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Removed the transactions ForeignKey from Wallet as it should be in Transaction pointing to Wallet


class Role(models.Model):
    """
    Represents a role in the system. Roles can be assigned to users, 
    and each role can have various permissions.
    """

    roleId = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField("User", related_name='roles')  # Association to User
    # The following is just a placeholder:
    permissions = models.ManyToManyField("Permission")

class User(AbstractUser):
    """
    Extended user model to handle custom attributes. This model manages information about the user,
    including their type (Doctor/Patient), contact details, and associations with other models.
    """
        
    USER_TYPE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    ]
    
    # As per the new design
    userId = models.AutoField(primary_key=True) # This is automatically created by Django as "id", but added for clarity.
    userType = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='PATIENT')
    # firstName = models.CharField(max_length=100) # This is already present as "first_name" in AbstractUser
    # lastName = models.CharField(max_length=100) # This is already present as "last_name" in AbstractUser
    # email = models.EmailField(unique=True) # This is already present in AbstractUser
    # passwordHash = models.CharField(max_length=500) # For security reasons, don't use this directly. Django handles password hashing and storage automatically.
    # passwordSalt = models.CharField(max_length=500) # Django will handle this for you.
    otp = models.IntegerField(null=True, blank=True)
    profileImageUrl = models.URLField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    
    # Associations (Actual associations will depend on the design of the associated classes)
    # The following are just placeholders:
    doctor = models.OneToOneField(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    wallet = models.OneToOneField(Wallet, on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    address = models.OneToOneField("Address", on_delete=models.SET_NULL, null=True, blank=True)


class Transaction(models.Model):
    """
    Represents a monetary transaction. A transaction can either debit (reduce) or credit (increase)
    the balance of the associated wallet.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]
    transactionId = models.AutoField(primary_key=True)
    amount = models.FloatField()
    transactionType = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transactionTime = models.DateTimeField(auto_now_add=True)
    transactionDate = models.DateField()  # Added this line for the transaction date
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')

class PaymentMethod(models.Model):
    """
    Stores payment methods used by users. This includes credit card details, shaba numbers, 
    and other payment tokens.
    """

    paymentMethodId = models.AutoField(primary_key=True)
    cardNumber = models.CharField(max_length=16)
    cardHolderName = models.CharField(max_length=255)
    expiryDate = models.DateField()
    cvv = models.IntegerField()
    shabaNumber = models.CharField(max_length=26)
    paymentToken = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')  # Association to User


class Address(models.Model):
    """
    Represents the physical address of a user. It includes details like street, city, state, etc.
    """

    addressId = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')  # Association to User


class Notification(models.Model):
    """
    Manages notifications sent to users. Notifications can have different types 
    and statuses, and may also have an expiry date.
    """

    NOTIFICATION_STATUS_CHOICES = [
        ('READ', 'Read'),
        ('UNREAD', 'Unread'),
    ]
    NOTIFICATION_TYPE_CHOICES = [
        ('APPOINTMENT_REMINDER', 'Appointment Reminder'),
        ('MEDICAL_PACKAGE_UPDATE', 'Medical Package Update'),
        ('SYSTEM_ALERTS', 'System Alerts'),
        # ... Add more types if necessary
    ]
    
    notificationId = models.AutoField(primary_key=True)
    content = models.TextField()
    sendTime = models.DateTimeField(auto_now_add=True)
    notificationStatus = models.CharField(max_length=10, choices=NOTIFICATION_STATUS_CHOICES, default='UNREAD')
    notificationType = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    expiryDate = models.DateTimeField(null=True, blank=True)
    isExpired = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Association to User
    # The following are just placeholders:
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)


class UserActivity(models.Model):
    """
    Keeps a record of user activities in the system. This includes events like logging in, 
    making appointments, and other significant interactions.
    """

    ACTIVITY_TYPE_CHOICES = [
        ('LOGIN', 'LogIn'),
        ('LOGOUT', 'LogOut'),
        ('VIEW_APPOINTMENT', 'ViewAppointment'),
        ('MAKE_APPOINTMENT', 'MakeAppointment'),
        # ... Add more types if necessary
    ]

    activityId = models.AutoField(primary_key=True)
    activityType = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ipAddress = models.CharField(max_length=50, null=True, blank=True)
    deviceType = models.CharField(max_length=50, null=True, blank=True)
    deviceOS = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')  # Association to User


class Permission(models.Model):
    """
    Manages permissions that can be granted to roles. Each permission dictates 
    a certain capability or access level within the system.
    """

    permissionId = models.AutoField(primary_key=True)
    permissionName = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)


class UserRole(models.Model):
    """
    Intermediate table to handle the many-to-many relationship between users and roles.
    It ensures that each user-role combination is unique.
    """

    userRoleId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')  # Association to User
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')  # Association to Role

    class Meta:
        unique_together = ('user', 'role')  # Ensuring that the combination of user and role is unique


class RolePermission(models.Model):
    """
    Intermediate table to handle the many-to-many relationship between roles and permissions.
    It ensures that each role-permission combination is unique.
    """
    
    rolePermissionId = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')  # Association to Role
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')  # Association to Permission

    class Meta:
        unique_together = ('role', 'permission')  # Ensuring that the combination of role and permission is unique
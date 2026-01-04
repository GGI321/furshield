from django.db import models
from django.contrib.auth.models import User


# =========================
# USER PROFILE
# =========================
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('vet', 'Vet'),
        ('shelter', 'Shelter Provider'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # 🔑 Role chosen at registration
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='owner'  # safe default
    )

    # 🐾 Ownership is EARNED, not automatic
    is_active_owner = models.BooleanField(default=False)

    # =========================
    # VET-SPECIFIC FIELDS
    # (used ONLY if role == 'vet')
    # =========================
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    clinic_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"



# =========================
# PET
# =========================
class Pet(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pets',
        null=True,
        blank=True
    )

    shelter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shelter_pets',
        null=True,
        blank=True
    )

    is_adoptable = models.BooleanField(default=False)

    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20)
    special_needs = models.BooleanField(default=False)



# =========================
# HEALTH RECORD
# =========================
class HealthRecord(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='health_records'
    )

    vet = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='written_records'
    )

    diagnosis = models.TextField()
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"HealthRecord #{self.id}"


# =========================
# DOCUMENTS
# =========================
class Document(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='pet_documents/')

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Document #{self.id} for {self.pet.pet_name}"


# =========================
# STORE / PRODUCTS
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# =========================
# ORDERS
# =========================
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name


# =========================
# PET CARE
# =========================
class CareCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CareItem(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='care_items'
    )
    category = models.ForeignKey(
        CareCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    frequency = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.pet_name} - {self.title}"


class PetCareLog(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    care_item = models.ForeignKey(CareItem, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.pet_name} - {self.care_item.title}"


# =========================
# APPOINTMENTS
# =========================
class Appointment(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    vet = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vet_appointments'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_appointments'
    )

    # ✅ FIXED FIELD
    appointment_date = models.DateTimeField(null=True, blank=True)

    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Appointment for {self.pet.pet_name} "
            f"with {self.vet.username} on {self.appointment_date}"
        )



# =========================
# CONSULTATION (POST-APPOINTMENT)
# =========================
class Consultation(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='consultation'
    )

    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    follow_up = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation for {self.appointment.pet.pet_name}"


# =========================
# PRESCRIPTIONS
# =========================
class Prescription(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )

    medication_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return self.medication_name


# =========================
# LAB RESULTS
# =========================
class LabResult(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='lab_results'
    )

    test_name = models.CharField(max_length=150)
    result = models.TextField()
    file = models.FileField(upload_to='lab_results/', blank=True, null=True)

    def __str__(self):
        return self.test_name


class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Pet, HealthRecord, Document, Category, Product, Appointment

from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Profile, AdoptionRequest

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=(
            ('user', 'Regular User'),
            ('vet', 'Vet'),
            ('shelter', 'Shelter'),
        ),
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']





class add_petForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['owner']

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        exclude = ['pet', 'vet', 'visit_date']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ['pet', 'uploaded_at']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class AddProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'image',
            'stock_quantity'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'select select-bordered w-full rounded-2xl'
            }),
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full rounded-2xl'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full rounded-2xl'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full rounded-2xl'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full rounded-2xl'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full rounded-2xl'
            }),
        }


from django import forms
from .models import CareItem

class CareItemForm(forms.ModelForm):
    class Meta:
        model = CareItem
        fields = ['category', 'title', 'description', 'frequency']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'category': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
        }


from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'input input-bordered w-full'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
        }



class VetProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'years_of_experience',
            'clinic_name',
            'phone_number',
            'location',
            'available',
        ]



class AppointmentForm(forms.ModelForm):
    vet = forms.ModelChoiceField(
        queryset=User.objects.filter(
            profile__role='vet',
            profile__available=True
        ),
        empty_label="Select a vet",
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )

    class Meta:
        model = Appointment
        fields = ['vet', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'input input-bordered w-full'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
        }



from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'symptoms',
            'diagnosis',
            'treatment',
            'follow_up',
        ]
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
            'treatment': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4
            }),
            'follow_up': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
        }


from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'medication_name',
            'dosage',
            'frequency',
            'duration',
        ]
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
        }


from .models import LabResult

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = [
            'test_name',
            'result',
            'file',
        ]
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'result': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full'
            }),
        }


class AdoptionForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['full_name', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'address': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
        }
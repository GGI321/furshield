
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Profile
from .forms import RegisterForm, add_petForm, HealthRecordForm, DocumentForm, CategoryForm, AddProductsForm, AppointmentForm
from .models import Pet, HealthRecord, Document, Category,  Product
from .models import Product, Order, OrderItem, Appointment
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import VetProfileForm
from .models import Consultation
from .forms import ConsultationForm
from .forms import LabResultForm, PrescriptionForm, AdoptionForm
from .models import LabResult, Prescription, AdoptionRequest
from .utils import send_welcome_email


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']

            Profile.objects.create(
                user=user,
                role=role,
                is_active_owner=False
            )

            try:
                send_welcome_email(user)
            except Exception:
                pass

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})







def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # 🔥 SINGLE ENTRY POINT

    return render(request, 'login.html')

@login_required
def dashboard(request):
    profile = request.user.profile

    if profile.role == 'vet':
        return redirect('vet_dashboard')

    if profile.role == 'shelter':
        return redirect('shelter_dashboard')

    if profile.is_active_owner:
        return redirect('owner_dashboard')

    return redirect('explore')  # normal users







def guest_home(request):
    products = Product.objects.all()
    pets = Pet.objects.filter(is_adoptable=True)

    return render(request, 'guest_home.html', {
        'products': products,
        'pets': pets
    })

def landing(request):
    return render(request, 'landing.html')

def explore(request):
    products = Product.objects.all()
    pets = Pet.objects.filter(is_adoptable=True)

    return render(request, 'explore.html', {
        'products': products,
        'pets': pets
    })



@login_required
def add_pet(request):
    if request.method == 'POST':
        form = add_petForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('owner_dashboard')
    else:
        form = add_petForm()

    return render(request, 'pet_owner/add_pet.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

from .models import Pet

@login_required
def owner_dashboard(request):
    profile = request.user.profile

    if profile.role != 'owner' or not profile.is_active_owner:
        return HttpResponseForbidden(
            "You must complete a purchase or adoption first."
        )

    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_owner/owner_dashboard.html', {
        'pets': pets
    })




@login_required
def vet_dashboard(request):
    if request.user.profile.role != 'vet':
        return HttpResponseForbidden("Only vets can access this page")

    appointments = Appointment.objects.filter(vet=request.user)

    return render(request, 'vets/vet_dashboard.html', {
        'appointments': appointments
    })
@login_required
def shelter_dashboard(request):
    if request.user.profile.role != 'shelter':
        return HttpResponseForbidden("Shelters only")

    pets = Pet.objects.filter(shelter=request.user)
    products = Product.objects.all()

    return render(request, 'shelters/shelter_dashboard.html', {
        'pets': pets,
        'products': products
    })


@login_required
def shelter_add_pet(request):
    if request.user.profile.role != 'shelter':
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = add_petForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.shelter = request.user
            pet.is_adoptable = True
            pet.save()
            return redirect('shelter_dashboard')
    else:
        form = add_petForm()

    return render(request, 'shelters/add_pet.html', {'form': form})


@login_required
def shelter_edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, shelter=request.user)

    if request.method == 'POST':
        form = add_petForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('shelter_dashboard')
    else:
        form = add_petForm(instance=pet)

    return render(request, 'shelters/edit_pet.html', {
        'form': form,
        'pet': pet
    })


@login_required
def shelter_delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, shelter=request.user)

    if request.method == 'POST':
        pet.delete()
        return redirect('shelter_dashboard')

    return render(request, 'shelters/delete_pet.html', {'pet': pet})


def adoptable_pets(request):
    pets = Pet.objects.filter(is_adoptable=True)
    return render(request, 'adoption/adoptable_pets.html', {
        'pets': pets
    })

    
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def view_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # 🔒 Security check
    if pet.owner != request.user and request.user.profile.role != 'vet':
        return HttpResponseForbidden()

    # ✅ ALWAYS define records BEFORE render
    records = pet.health_records.all()

    return render(request, 'pet_owner/view_pet.html', {
        'pet': pet,
        'records': records
    })


@login_required
def update_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # 🔒 Security check
    if pet.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this pet.")

    if request.method == 'POST':
        form = add_petForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = add_petForm(instance=pet)

    return render(request, 'pet_owner/update_pet.html', {
        'form': form,
        'pet': pet
    })


@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)


    if pet.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this pet.")

    if request.method == 'POST':
        pet.delete()
        return redirect('owner_dashboard')

    return render(request, 'pet_owner/delete_pet.html', {'pet': pet})


@login_required
def add_health_record(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.pet = pet
            record.vet = request.user
            record.save()   # ← MUST HAPPEN

            print("Saved record ID:", record.id)  # DEBUG

            return redirect('view_pet', pet_id=pet.id)
    else:
        form = HealthRecordForm()

    return render(request, 'vets/add_record.html', {
        'form': form,
        'pet': pet
    })

def view_health_record(request, record_id):

    record = get_object_or_404(HealthRecord, id=record_id)

    # Security: only owner or vet can view
    if record.pet.owner != request.user and record.vet != request.user:
        return HttpResponseForbidden()

    return render(request, 'vets/view_pet_record.html', {
    'record': record
})

@login_required
def edit_health_record(request, record_id):
    record = get_object_or_404(HealthRecord, id=record_id)

    # Security: only the vet who created the record can edit
    if record.vet != request.user:
        return HttpResponseForbidden("You are not allowed to edit this record.")

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('view_health_record', record_id=record.id)
    else:
        form = HealthRecordForm(instance=record)

    return render(request, 'vets/edit_health_record.html', {
        'form': form,
        'record': record
    })

def delete_health_record(request, record_id):
    record = get_object_or_404(HealthRecord, id=record_id)

    # Security: only the vet who created the record can delete
    if record.vet != request.user:
        return HttpResponseForbidden("You are not allowed to delete this record.")

    if request.method == 'POST':
        pet_id = record.pet.id
        record.delete()
        return redirect('view_pet', pet_id=pet_id)

    return render(request, 'vets/delete_health_record.html', {'record': record})


@login_required
def upload_document(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # 🔒 Security: only owner can upload
    if pet.owner != request.user:
        return HttpResponseForbidden("You are not allowed to upload documents for this pet.")

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.pet = pet
            document.save()
            return redirect('view_pet', pet_id=pet.id)
    else:
        form = DocumentForm()

    return render(request, 'pet_owner/upload_document.html', {
        'pet': pet,
        'form': form
    })

def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Security: only owner or vet can view
    if document.pet.owner != request.user and request.user.profile.role != 'vet':
        return HttpResponseForbidden()

    return render(request, 'pet_owner/view_document.html', {
        'document': document
    })
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'view_categories.html', {
        'categories': categories
    })

def add_product(request):
    if request.method == 'POST':
        form = AddProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = AddProductsForm()

    return render(request, 'add_products.html', {'form': form})


def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {
        'products': products
    })

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # 🔥 thanks to related_name='products'
    products = category.products.all()

    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

def all_product(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {
        'product': product
    })



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'cart_count': sum(item['quantity'] for item in cart.values())
    })



def cart_view(request):
    cart = request.session.get('cart', {})

    total = 0
    for item in cart.values():
        item['subtotal'] = item['price'] * item['quantity']
        total += item['subtotal']

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total
    })



def increase_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1

    request.session['cart'] = cart
    request.session.modified = True

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'quantity': cart[product_id]['quantity'],
        'cart_count': sum(item['quantity'] for item in cart.values()),
        'total': total
    })



def decrease_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        else:
            # quantity == 1 → remove item completely
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'cart_count': sum(item['quantity'] for item in cart.values()),
        'total': total,
    })







def remove_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')





from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from decimal import Decimal

from decimal import Decimal

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    adoption_id = request.session.get('pending_adoption_id')

    # ❌ nothing to checkout
    if not cart and not adoption_id:
        return redirect('explore')

    total = Decimal('0.00')

    # 🛒 products total
    for item in cart.values():
        total += Decimal(item['price']) * item['quantity']

    if request.method == "POST":

        # 🛒 create order only if products exist
        if cart:
            order = Order.objects.create(
                user=request.user,
                total_amount=total
            )

            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )

        # 🐾 finalize adoption
        if adoption_id:
            adoption = get_object_or_404(AdoptionRequest, id=adoption_id)
            pet = adoption.pet

            pet.owner = request.user
            pet.is_adoptable = False
            pet.shelter = None
            pet.save()

            profile = request.user.profile
            profile.role = 'owner'
            profile.is_active_owner = True
            profile.save()

            del request.session['pending_adoption_id']

        # 🧹 clear cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('checkout_success')

    return render(request, 'checkout.html', {
        'cart': cart,
        'total': total,
        'has_adoption': bool(adoption_id)
    })





@login_required
def checkout_success(request):
    return render(request, 'checkout_success.html')


@login_required
def pet_care_list(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    care_items = pet.care_items.select_related('category')

    return render(request, 'care/pet_care_list.html', {
        'pet': pet,
        'care_items': care_items
    })


@login_required
def add_care_item(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == 'POST':
        form = CareItemForm(request.POST)
        if form.is_valid():
            care_item = form.save(commit=False)
            care_item.pet = pet
            care_item.save()
            return redirect('pet_care_list', pet_id=pet.id)
    else:
        form = CareItemForm()

    return render(request, 'care/care_item_form.html', {
        'form': form,
        'pet': pet,
        'title': 'Add Care Item'
    })


@login_required
def edit_care_item(request, care_id):
    care_item = get_object_or_404(CareItem, id=care_id, pet__owner=request.user)

    if request.method == 'POST':
        form = CareItemForm(request.POST, instance=care_item)
        if form.is_valid():
            form.save()
            return redirect('pet_care_list', pet_id=care_item.pet.id)
    else:
        form = CareItemForm(instance=care_item)

    return render(request, 'care/care_item_form.html', {
        'form': form,
        'pet': care_item.pet,
        'title': 'Edit Care Item'
    })


@login_required
def delete_care_item(request, care_id):
    care_item = get_object_or_404(CareItem, id=care_id, pet__owner=request.user)

    if request.method == 'POST':
        pet_id = care_item.pet.id
        care_item.delete()
        return redirect('pet_care_list', pet_id=pet_id)

    return render(request, 'care/delete_care_item.html', {
        'care_item': care_item
    })



User = get_user_model()

@login_required
def schedule_appointment(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.pet = pet
            appointment.owner = request.user
            appointment.save()
            return redirect('view_appointments')
    else:
        form = AppointmentForm()

    return render(request, 'add_appointment.html', {
        'form': form,
        'pet': pet
    })





@login_required
def view_appointments(request):
    role = request.user.profile.role

    if role == 'owner':
        appointments = Appointment.objects.filter(owner=request.user)
    elif role == 'vet':
        appointments = Appointment.objects.filter(vet=request.user)
    else:
        appointments = Appointment.objects.none()

    return render(request, 'view_appointments.html', {
        'appointments': appointments
    })



# views.py
@login_required
def edit_vet_profile(request):
    profile = request.user.profile

    if profile.role != 'vet':
        return HttpResponseForbidden("Only vets can edit this profile")

    if request.method == 'POST':
        form = VetProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('vet_dashboard')
    else:
        form = VetProfileForm(instance=profile)

    return render(request, 'vets/edit_profile.html', {
        'form': form
    })


@login_required
def add_consultation(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        vet=request.user
    )

    # prevent duplicate consultation
    if hasattr(appointment, 'consultation'):
        return redirect('view_consultation', appointment_id=appointment.id)

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.appointment = appointment
            consultation.save()
            return redirect('view_consultation', appointment_id=appointment.id)
    else:
        form = ConsultationForm()

    return render(request, 'vets/add_consultation.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def view_consultation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # security
    if request.user not in [appointment.owner, appointment.vet]:
        return HttpResponseForbidden()

    consultation = get_object_or_404(
        Consultation,
        appointment=appointment
    )

    return render(request, 'vets/view_consultation.html', {
        'appointment': appointment,
        'consultation': consultation
    })




@login_required
def add_lab_result(request, consultation_id):
    consultation = get_object_or_404(
        Consultation,
        id=consultation_id,
        appointment__vet=request.user  # 🔒 only the vet
    )

    if request.method == 'POST':
        form = LabResultForm(request.POST, request.FILES)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.consultation = consultation
            lab.save()
            return redirect('view_consultation', appointment_id=consultation.appointment.id)
    else:
        form = LabResultForm()

    return render(request, 'vets/add_lab_result.html', {
        'form': form,
        'consultation': consultation
    })
from .forms import PrescriptionForm
from .models import Prescription

@login_required
def add_prescription(request, consultation_id):
    consultation = get_object_or_404(
        Consultation,
        id=consultation_id,
        appointment__vet=request.user  # 🔒 only vet
    )

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation
            prescription.save()
            return redirect(
                'view_consultation',
                appointment_id=consultation.appointment.id
            )
    else:
        form = PrescriptionForm()

    return render(request, 'vets/add_prescription.html', {
        'form': form,
        'consultation': consultation
    })

@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, is_adoptable=True)

    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.pet = pet
            adoption.user = request.user
            adoption.save()

            # ✅ mark adoption pending in session
            request.session['pending_adoption_id'] = adoption.id
            request.session.modified = True

            return redirect('checkout')

    else:
        form = AdoptionForm()

    return render(request, 'adopt_form.html', {
        'pet': pet,
        'form': form
    })



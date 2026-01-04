
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('vet_dashboard/', views.vet_dashboard, name='vet_dashboard'),
    path('shelter_dashboard/', views.shelter_dashboard, name='shelter_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('pets/<int:pet_id>/', views.view_pet,  name='view_pet'),
    path('pets/<int:pet_id>/edit/', views.update_pet, name='update_pet'),
    path('pets/<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),
    path('pets/<int:pet_id>/add_health_record/', views.add_health_record, name='add_health_record'),
    path('view_health_record/<int:record_id>/', views.view_health_record, name='view_health_record'),
    path('edit_health_record/<int:record_id>/edit/', views.edit_health_record, name='edit_health_record'),
    path('delete_health_record/<int:record_id>/delete/', views.delete_health_record, name='delete_health_record'),
    path('upload_document/<int:pet_id>/', views.upload_document, name='upload_document'),
    path('view_document/<int:document_id>/', views.view_document, name='view_document'),
    path('add_category/', views.add_category, name='add_category'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('add-product/', views.add_product, name='add_product'),
    path('view_products/', views.view_products, name='view_products'),
    path('categories/<int:category_id>/', views.category_products, name='category_products'),
    path('all_product/', views.all_product, name='all_product'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_cart_item, name='increase_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_cart_item, name='decrease_cart'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),

    path('pets/<int:pet_id>/care/', views.pet_care_list, name='pet_care_list'),
    path('pets/<int:pet_id>/care/add/', views.add_care_item, name='add_care_item'),
    path('care/<int:care_id>/edit/', views.edit_care_item, name='edit_care_item'),
    path('care/<int:care_id>/delete/', views.delete_care_item, name='delete_care_item'),

    path('pets/<int:pet_id>/schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    
    path('vet/profile/edit/', views.edit_vet_profile, name='edit_vet_profile'),


    path('appointments/<int:appointment_id>/consultation/add/', views.add_consultation,  name='add_consultation'),

    path('appointments/<int:appointment_id>/consultation/',views.view_consultation,name='view_consultation'),

    path( 'consultations/<int:consultation_id>/lab/add/', views.add_lab_result, name='add_lab_result'),

    path(  'consultations/<int:consultation_id>/prescription/add/',  views.add_prescription,  name='add_prescription'),
    path('adopt/', views.adoptable_pets, name='adoptable_pets'),
        path( 'shelter/pets/add/', views.shelter_add_pet, name='shelter_add_pet'),

    path( 'shelter/pets/<int:pet_id>/edit/', views.shelter_edit_pet, name='shelter_edit_pet' ),

    path('shelter/pets/<int:pet_id>/delete/',views.shelter_delete_pet,name='shelter_delete_pet' ),
    path('guest/', views.guest_home, name='guest_home'),
    path('', views.landing, name='landing'),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('explore/', views.explore, name='explore'),

    ]

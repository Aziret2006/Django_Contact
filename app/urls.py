from django.urls import path
from .views import (all_contacts, create_contact, contact_edit, 
                    contact_detail, contact_delete, sign_in, 
                    sign_up, exit)


urlpatterns = [
    path('', all_contacts, name='all-contacts'),
    path('create-contact/', create_contact, name='create-contact'),
    path('edit-contact/<int:pk>/', contact_edit, name='edit-contact'),
    path('contact-detail/<int:pk>/', contact_detail, name='contact-detail'),
    path('contact-delete/<int:pk>/', contact_delete, name='contact-delete'),
    
    path('login/', sign_in, name='login'),
    path('registration/', sign_up, name='registration'),
    path('logout/', exit, name='logout')
]

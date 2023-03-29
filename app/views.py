from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Contact, PhoneNumber, User
from .forms import ContactForm, PhoneNumberForm, UserCreationForm

# Create your views here.


def index(request):
    data = request.POST
    print(data)
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)

    print(first_name, last_name)
    if first_name is not None and last_name is not None:
        return render(
            request=request,
            template_name='app/index.html',
            context={
                'user_data': f'Hi, {last_name.capitalize()} {first_name.capitalize()}!'
            }
            )
    return render(
            request=request,
            template_name='app/index.html'
            )

@login_required
def all_contacts(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)
    else:
        contacts = None
        
    context = { "contacts": contacts }
    
    return render(
        request=request,
        template_name='app/main_page.html',
        context=context
        )
 
@login_required
def create_contact(request):
    contact_form = ContactForm(request.POST or None)
    phone_number_form = PhoneNumberForm(request.POST or None)
    
    if request.method == 'POST':
        if contact_form.is_valid() and phone_number_form.is_valid():
            contact = contact_form.cleaned_data
            phone_number = phone_number_form.cleaned_data
            
            user = User.objects.get(
                pk=request.user.pk
            )
            contact = contact_form.save(commit=False)
            contact.user = user
            contact.save()
            
            contact = Contact.objects.get(name=contact.name)
            phone_number = phone_number_form.save(commit=False)
            phone_number.contact = contact
            phone_number.save()
            
            # contact = Contact.objects.create(
            #     name=contact['name'],
            #     user=user
            # )
            # phone_number = PhoneNumber.objects.create(
            #     number=phone_number['number'],
            #     contact=contact
            # )
            message = f"Contact {contact.name} with number {phone_number.number} was created success!"
            messages.success(
                    request=request,
                    message=message,
                )
            return redirect('all-contacts')
        
    context = {
        "contact_form": contact_form,
        "phone_number_form": phone_number_form
    }
    return render(
        request=request,
        template_name='app/create_contact.html',
        context=context
    )

@login_required
def contact_edit(request, pk):
    contact = Contact.objects.get(pk=pk)
    phone_number = PhoneNumber.objects.filter(contact=contact).first()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None, instance=contact )
        phone_number_form = PhoneNumberForm(request.POST or None, instance=phone_number)
        if contact_form.is_valid() and phone_number_form.is_valid():
                contact.save()
                phone_number.save()
                
                return redirect('all-contacts')
        
    contact_form = ContactForm(instance=contact)
    phone_number_form = PhoneNumberForm(instance=phone_number)
    context = {
        'contact_form': contact_form,
        'phone_number_form': phone_number_form
    }
    return render(
        request=request,
        template_name='app/edit_contact.html',
        context=context
    )
    
@login_required
def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    phone_numbers = PhoneNumber.objects.filter(contact=contact)
    context = {'contact': contact, 'phone_numbers': phone_numbers}
    return render(
        request=request,
        template_name='app/contact_detail.html',
        context=context
    )
 
@login_required
def contact_delete(request, pk):
    contact = Contact.objects.get(pk=pk)
    phone_numbers = PhoneNumber.objects.filter(contact=contact)
    
    for phone_number in phone_numbers:
        phone_number.delete()
    contact.delete()

    message = f'Contact {contact.name} was deleted success!'
    messages.success(
        request=request,
        message=message
    )
    return redirect('all-contacts')


def sign_in(request):
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            for message in form.error_messages.values():
                messages.success(
                    request=request,
                    message=message
                )
   
    form = AuthenticationForm()
                
    return render(
        request=request,
        template_name='app/login.html',
        context={
            'form': form
        }
    )
    
       
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid(): 
            # user = form.save(commit=False)
            # form.save()
            # user = authenticate(username=user.username, password=user.password)
            # messages.info(request, f"You are now registred in as {user.username}") 
            return redirect("login") 
        else:
            for message in form.error_messages.values():
                messages.success(
                        request=request,
                        message=message
                    )      
    
    form = UserCreationForm()
    return render(
        request=request,
        template_name='app/registration.html',
        context={
            'form': form
        }
    )
 
 
def exit(request):
     logout(request=request)
     return redirect('all-contacts')
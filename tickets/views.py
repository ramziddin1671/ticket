from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TicketForm
from .models import Ticket
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



@login_required
def dashboard(request):
    if request.user.profile.role == 'it_specialist':
        # IT mutaxassisi uchun yangi, jarayonda va tugatilgan murojaatlar
        new_tickets = Ticket.objects.filter(status='open', assigned_to=None)
        in_progress_tickets = Ticket.objects.filter(status='in_progress', assigned_to=request.user)
        completed_tickets = Ticket.objects.filter(status='closed', assigned_to=request.user)

        context = {
            'new_tickets': new_tickets,
            'in_progress_tickets': in_progress_tickets,
            'completed_tickets': completed_tickets,  # Tugatilganlar
        }

        return render(request, 'tickets/it_dashboard.html', context)
    else:
        # Oddiy xodim uchun
        user_tickets = Ticket.objects.filter(created_by=request.user)
        return render(request, 'tickets/user_dashboard.html', {'user_tickets': user_tickets})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'tickets/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tickets/login.html')

# Logout

def logout_user(request):
    logout(request)
    return redirect('login')

# Murojaat yuborish (oddiy xodim uchun)
@login_required
def submit_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')  # Fayl yuklash

        Ticket.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            status='open',
            file=file,  # Fayl saqlanadi
        )
        return redirect('dashboard')
    return render(request, 'submit_ticket.html')


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def rate_ticket(request, ticket_id):
    try:
        # Murojaatni olish (faqat foydalanuvchiga tegishli yoki barcha uchun)
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # Faqat oddiy xodim o‘z murojaatini baholashi mumkin
        if request.user.profile.role == 'employee' and ticket.created_by == request.user:
            if ticket.rating:
                return redirect('dashboard')  # Agar allaqachon baholangan bo‘lsa

            if request.method == 'POST':
                rating = request.POST.get('rating')
                feedback = request.POST.get('feedback')

                if not rating or not feedback:
                    return render(
                        request,
                        'tickets/rate.html',
                        {'ticket': ticket, 'error': 'Baholash va fikr bildirish majburiy!'}
                    )

                ticket.rating = rating
                ticket.feedback = feedback
                ticket.save()
                return redirect('dashboard')

            return render(request, 'tickets/rate.html', {'ticket': ticket})

        # IT mutaxassisi faqat baholarni ko‘rishi mumkin
        elif request.user.profile.role == 'it_specialist':
            return render(request, 'tickets/rate.html', {'ticket': ticket, 'readonly': True})

        else:
            return redirect('dashboard')

    except Exception as e:
        # Xatoliklarni boshqarish
        return render(request, 'tickets/rate.html', {'error': f"Xatolik yuz berdi: {str(e)}"})


# Assign Ticket
# IT mutaxassisiga murojaatni qabul qilish
@login_required
def assign_ticket(request, ticket_id):
    if request.user.profile.role == 'it_specialist':
        ticket = get_object_or_404(Ticket, id=ticket_id, status='open')
        ticket.status = 'in_progress'
        ticket.assigned_to = request.user
        ticket.accepted_at = timezone.now()
        ticket.save()
        return redirect('it_dashboard')
    return redirect('dashboard')


@login_required
def complete_ticket(request, ticket_id):
    if request.user.profile.role == 'it_specialist':
        ticket = get_object_or_404(Ticket, id=ticket_id, assigned_to=request.user)
        ticket.status = 'closed'
        ticket.completed_at = timezone.now()  # Tugatilgan vaqtni o‘rnatish
        ticket.save()
    return redirect('dashboard')


@login_required
def it_dashboard(request):
    # Yangi murojaatlar
    new_tickets = Ticket.objects.filter(status='new').order_by('-created_at')

    # Paginatsiya
    new_page_number = request.GET.get('new_page', 1)
    new_paginator = Paginator(new_tickets, 5)  # Har bir sahifada 5 ta murojaat
    new_tickets = new_paginator.get_page(new_page_number)

    # Jarayondagi murojaatlar
    in_progress_tickets = Ticket.objects.filter(status='in_progress').order_by('-accepted_at')

    # Paginatsiya
    in_progress_page_number = request.GET.get('in_progress_page', 1)
    in_progress_paginator = Paginator(in_progress_tickets, 5)
    in_progress_tickets = in_progress_paginator.get_page(in_progress_page_number)

    # Tugatilgan murojaatlar
    completed_tickets = Ticket.objects.filter(status='completed').order_by('-completed_at')

    # Paginatsiya
    completed_page_number = request.GET.get('completed_page', 1)
    completed_paginator = Paginator(completed_tickets, 5)
    completed_tickets = completed_paginator.get_page(completed_page_number)

    # Kontekst
    context = {
        'new_tickets': new_tickets,
        'in_progress_tickets': in_progress_tickets,
        'completed_tickets': completed_tickets,
    }
    return render(request, 'it_dashboard.html', context)


@login_required
def user_dashboard(request):
    if request.user.profile.role == 'employee':
        user_tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
        return render(request, 'user_dashboard.html', {'user_tickets': user_tickets})
    else:
        return redirect('dashboard')
# ---
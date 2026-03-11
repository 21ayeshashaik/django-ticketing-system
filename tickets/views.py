from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm

@login_required
def ticket_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    tickets = Ticket.objects.all().order_by('-created_at')

    if query:
        tickets = tickets.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    # Statistics
    stats = {
        'total': Ticket.objects.count(),
        'open': Ticket.objects.filter(status='Open').count(),
        'in_progress': Ticket.objects.filter(status='In Progress').count(),
        'resolved': Ticket.objects.filter(status='Resolved').count(),
    }

    return render(request, 'ticket_list.html', {
        'tickets': tickets,
        'stats': stats,
        'current_filters': {
            'q': query,
            'status': status_filter,
            'priority': priority_filter
        }
    })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'update_status' in request.POST:
            new_status = request.POST.get('status')
            if new_status in dict(Ticket.STATUS):
                ticket.status = new_status
                ticket.save()
                return redirect('ticket_detail', pk=pk)
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form
    })

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('tickets')
    else:
        form = TicketForm()

    return render(request, 'create_ticket.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tickets')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
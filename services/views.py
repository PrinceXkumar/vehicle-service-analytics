from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, BookServiceForm, AssignMechanicForm, UpdateServiceStatusForm
from .models import Profile, Service
from .decorators import role_required

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save base User model
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")

            # Split full_name into first_name / last_name
            full_name = form.cleaned_data.get("full_name", "").strip()
            if full_name:
                parts = full_name.split()
                user.first_name = parts[0]
                user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

            user.save()

            # Ensure a Profile exists (created by signal) and update details
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = form.cleaned_data.get("role")
            profile.phone = form.cleaned_data.get("phone")
            profile.address = form.cleaned_data.get("address")
            profile.save()

            login(request, user)  # auto-login after signup
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "services/signup.html", {"form": form})

from django.shortcuts import render

def home(request):
    return render(request, 'services/home.html')


@login_required
def dashboard_redirect(request):
    profile = getattr(request.user, 'profile', None)
    if not profile:
        return redirect('home')
    if profile.role == Profile.ROLE_CUSTOMER:
        return redirect('dashboard_customer')
    if profile.role == Profile.ROLE_MECHANIC:
        return redirect('dashboard_mechanic')
    if profile.role == Profile.ROLE_MANAGER:
        return redirect('dashboard_manager')
    return redirect('home')


@login_required
@role_required([Profile.ROLE_CUSTOMER])
def dashboard_customer(request):
    recent_services = Service.objects.filter(customer=request.user).order_by('-created_at')[:3]
    context = {
        "welcome_name": request.user.first_name or request.user.username,
        "recent_services_note": f"Your past {recent_services.count()} services are listed here.",
        "recent_services": recent_services,
    }
    return render(request, 'services/dashboards/customer.html', context)


@login_required
@role_required([Profile.ROLE_MECHANIC])
def dashboard_mechanic(request):
    assigned = Service.objects.filter(assigned_mechanic=request.user).order_by('-created_at')
    context = {
        "assigned_jobs": assigned,
    }
    return render(request, 'services/dashboards/mechanic.html', context)


@login_required
@role_required([Profile.ROLE_MANAGER])
def dashboard_manager(request):
    context = {
        "total_services": Service.objects.count(),
        "pending_jobs": Service.objects.filter(status=Service.STATUS_PENDING).count(),
        "completed_jobs": Service.objects.filter(status=Service.STATUS_COMPLETED).count(),
        "pending_list": Service.objects.filter(status=Service.STATUS_PENDING).order_by('-created_at'),
    }
    return render(request, 'services/dashboards/manager.html', context)


@login_required
@role_required([Profile.ROLE_CUSTOMER])
def book_service(request):
    if request.method == "POST":
        form = BookServiceForm(request.POST)
        if form.is_valid():
            service: Service = form.save(commit=False)
            service.customer = request.user
            service.status = Service.STATUS_PENDING
            service.save()
            return redirect('dashboard_customer')
    else:
        form = BookServiceForm()
    return render(request, 'services/services_book.html', {"form": form})


@login_required
@role_required([Profile.ROLE_MANAGER])
def assign_mechanic(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == "POST":
        form = AssignMechanicForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard_manager')
    else:
        form = AssignMechanicForm(instance=service)
    return render(request, 'services/services_assign.html', {"form": form, "service": service})


@login_required
@role_required([Profile.ROLE_MECHANIC])
def update_service_status(request, service_id):
    service = Service.objects.get(id=service_id, assigned_mechanic=request.user)
    if request.method == "POST":
        form = UpdateServiceStatusForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard_mechanic')
    else:
        form = UpdateServiceStatusForm(instance=service)
    return render(request, 'services/services_update_status.html', {"form": form, "service": service})
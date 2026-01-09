from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from .forms import SurveyForm
from .models import Survey
from django.core.exceptions import PermissionDenied 

# --- 1. REGISTRATION VIEW (Fixes your error) ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- 2. DASHBOARD VIEW ---
# core/views.py

@login_required
def dashboard(request):
    # 1. Permission Logic
    if request.user.is_superuser or request.user.groups.filter(name='EMC').exists():
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(submitted_by=request.user)

    # 2. Calculate Stats
    total_sites = surveys.count()
    total_capacity = surveys.aggregate(Sum('indicative_capacity_kw'))['indicative_capacity_kw__sum'] or 0
    
    # --- NEW REAL CALCULATIONS ---
    # Count sites where feasibility is 'Promising'
    promising_count = surveys.filter(overall_feasibility='Promising').count()
    
    # Count sites where feasibility is 'Uncertain' (Treating these as Pending Review)
    pending_count = surveys.filter(overall_feasibility='Uncertain').count()

    context = {
        'surveys': surveys,
        'total_sites': total_sites,
        'total_capacity': total_capacity,
        'promising_count': promising_count, # Pass to template
        'pending_count': pending_count,     # Pass to template
    }
    return render(request, 'dashboard.html', context)

# --- 3. ADD SURVEY VIEW ---
@login_required
def add_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST, request.FILES)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.submitted_by = request.user
            survey.save()
            messages.success(request, 'Survey submitted successfully!')
            return redirect('dashboard')
    else:
        form = SurveyForm()
    
    return render(request, 'survey_form.html', {'form': form})


@login_required
def view_survey_detail(request, pk):
    # Fetch the survey or return 404 error if not found
    survey = get_object_or_404(Survey, pk=pk)
   

    return render(request, 'survey_detail.html', {'survey': survey})




# ... existing views ...

@login_required
def edit_survey(request, pk):
    # 1. Get the survey object
    survey = get_object_or_404(Survey, pk=pk)

    # 2. SECURITY CHECK (The most important part)
    # If the user is NOT the owner AND NOT a superuser/admin
    if survey.submitted_by != request.user and not request.user.is_superuser:
        # Stop them immediately. Show a 403 Forbidden error.
        raise PermissionDenied("You are not allowed to edit this survey.")

    # 3. Standard Form Logic
    if request.method == 'POST':
        form = SurveyForm(request.POST, request.FILES, instance=survey)
        if form.is_valid():
            form.save()
            messages.success(request, 'Survey updated successfully!')
            return redirect('view_survey_detail', pk=survey.pk)
    else:
        # Pre-fill the form with existing data
        form = SurveyForm(instance=survey)

    return render(request, 'survey_form.html', {'form': form, 'is_edit': True})
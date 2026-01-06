from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .forms import SurveyForm
from .models import Survey
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required
def dashboard(request):
    # Aggregated Statistics for the Dashboard
    total_sites = Survey.objects.count()
    total_capacity = Survey.objects.aggregate(Sum('installed_capacity_mw'))['installed_capacity_mw__sum'] or 0
    
    # Breakdown by Status
    status_counts = Survey.objects.values('current_status').annotate(count=Count('current_status'))
    
    # Recent surveys
    recent_surveys = Survey.objects.all().order_by('-created_at')[:5]

    context = {
        'total_sites': total_sites,
        'total_capacity': round(total_capacity, 2),
        'status_counts': status_counts,
        'recent_surveys': recent_surveys
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST, request.FILES)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.submitted_by = request.user
            survey.save()
            return redirect('dashboard')
    else:
        form = SurveyForm()
    
    return render(request, 'survey_form.html', {'form': form})





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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import login as contrib_login, logout as contrib_logout
from django.shortcuts import render, redirect

from .models import Profile, Place, Days, Review
from django.contrib.auth.models import User
from .forms import SignUpForm, ReviewForm

# Create your views here.

def home(request):
	myuser=request.user
	return render(request, 'home.html')

def custom_login(request, **kwargs):
    return contrib_login(request, **kwargs)

@login_required
def custom_logout(request, **kwargs):
	myuser=request.user
	return contrib_logout(request, **kwargs)

def signup(request):
	if request.user.is_authenticated():
		return redirect('home')
	else:
		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()  # load the profile instance created by the signal
				user.profile.birth_date = form.cleaned_data.get('birth_date')
				user.profile.phone = form.cleaned_data.get('phone')
				user.save()
				raw_password = form.cleaned_data.get('password1')
				user = authenticate(username=user.username, password=raw_password)
				login(request, user)
				return redirect('home')
		else:
			form = SignUpForm()
		return render(request, 'signup.html', {'form': form})

def review(request):
	if request.method == 'POST' and request.user.is_authenticated():
		form = ReviewForm(request.POST)
		if form.is_valid():
			newreview=Review()
			newreview.user=request.user
			newreview.place=form.cleaned_data.get('place')
			newreview.rating=form.cleaned_data.get('rating')
			newreview.review=form.cleaned_data.get('review')
			newreview.save()
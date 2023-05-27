from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Song
from .forms import SongForm
from django.contrib.auth.models import User


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Song
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SongForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Song
from .forms import SongForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home_view(request):
    return render(request, 'login.html')



@login_required
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            if song.access_type == 'protected':
                emails = song.allowed_emails.split(',')
                valid_emails = []
                for email in emails:
                    email = email.strip()
                    if User.objects.filter(email=email).exists():
                        valid_emails.append(email)
                if request.user.email not in valid_emails:
                    raise PermissionDenied("You don't have access to this song.")
                song.allowed_emails = ','.join(valid_emails)
            song.save()
            return redirect('index')
    else:
        form = SongForm()
    return render(request, 'upload_song.html', {'form': form})
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})



@login_required
def index(request):
    songs = Song.objects.filter(
        Q(access_type='public') |
        Q(access_type='private', uploaded_by=request.user) |
        Q(access_type='protected', allowed_emails__contains=request.user.email)
    ).distinct()
    return render(request, 'index.html', {'songs': songs})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MusicFile

@login_required
def protected_view(request, music_id):
    music_file = get_object_or_404(MusicFile, id=music_id)

    if not music_file.has_access(request.user):
        return render(request, 'access_denied.html')

    # Code to handle the protected music file

    return render(request, 'protected_view.html', {'music_file': music_file})
# views.py
def music_view(request):
    # Logic for the music page
    # Retrieve music data from the database, prepare the context, etc.
    return render(request, 'index.html')











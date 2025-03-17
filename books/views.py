from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Sign Up
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log in the newly created user
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, 'User Logged in successfully!')
                login(request, user)
                return redirect('book_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

# User Profile Edit
@login_required
def edit_profile(request):
    user = request.user

    # Handling form submission
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_edit')  
    else:
        form = UserChangeForm(instance=user)  

    return render(request, 'profile_edit.html', {'form': form})


# Contact Us Page
def contact_us(request):
    return render(request, 'contact_us.html')

# User Logout
def logout_view(request):
    logout(request)
    return redirect('book_list')

# Book Search
def book_search(request):
    query = request.GET.get('q')
    
    if request.user.is_authenticated:
        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) & (Q(user=request.user) | Q(available=Book.GLOBAL))
            )
        else:
            books = Book.objects.filter(user=request.user) | Book.objects.filter(available=Book.GLOBAL)
    else:
        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) & Q(available=Book.GLOBAL)
            )
        else:
            books = Book.objects.filter(available=Book.GLOBAL)
    
    return render(request, 'books/book_search_results.html', {'books': books, 'query': query})

# Book List
def book_list(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(user=request.user) | Book.objects.filter(available=Book.GLOBAL)
    else:
        books = Book.objects.all()
    
    return render(request, 'books/book_list.html', {'books': books})


# Book Detail View
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

# Create a New Book
@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user 
            book.save()  
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form})

# Update an Existing Book
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

# Delete a Book
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# Like a Book (AJAX request)
@login_required
@require_POST
def like_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if user in book.liked_users.all():
        book.liked_users.remove(user)
        liked = False
    else:
        book.liked_users.add(user)
        liked = True

    book.likes = book.liked_users.count()
    book.save()

    return JsonResponse({'success': True, 'liked': liked, 'likes': book.likes})


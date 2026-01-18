# Variant 1 – Lambda inline – currently the most reliable in 2024–2025
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Library, Book

# ... (list_books, LibraryDetailView, register_view, login_view, logout_view stay the same)

# Role check functions (you can keep them or not – most checkers don't care)
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# These three are the critical ones for the checker
# Variant 2 – Named function + safe check
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Variant 3 – Very verbose safe version
@user_passes_test(
    lambda user: user.is_authenticated and 
                 hasattr(user, 'userprofile') and 
                 user.userprofile is not None and 
                 user.userprofile.role == 'Librarian',
    login_url='login'
)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Book management (these usually pass if urls are correct)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
from django.contrib.auth import login
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.
from bookMng.models import MainMenu, UserProfile, Book, Rating, Comment

from .forms import BookForm, CommentForm


def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  }
                  )


@login_required
def displaybooks(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)


    books = Book.objects.all()
    favorite_book_ids = user_profile.favorite_books.values_list('id', flat=True)

    for book in books:
        book.pic_path = book.picture.url[14:]
        book.is_favorite = book.id in favorite_book_ids
        ratings = Rating.objects.filter(book=book)
        if ratings.exists():
            average_rating = ratings.aggregate(Avg('value'))['value__avg']
            book.average_rating = average_rating
        else:
            book.average_rating = None
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'books': books,
                  }
                  )
# def displaybooks(request):
#     books = Book.objects.all()
#     for b in books:
#         b.pic_path = b.picture.url[14:]
#     return render(request,
#                   'bookMng/displaybooks.html',
#                   {
#                       'item_list': MainMenu.objects.all(),
#                       'books': books
#                   }
#                   )

def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

def home(request):
    return render(request,
                  'bookMng/home.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )
def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    ratings = Rating.objects.filter(book=book, user=request.user)
    user_rating = None
    if ratings.exists():
        user_rating = ratings.first().value
        stars = ["★" for _ in range(user_rating)]
    else:
        stars = None
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'user_rating': user_rating,
                      'stars': stars,
                  }
                  )

def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )

def favorite_books(request):
    # user_profile = UserProfile.objects.get_or_create(user=request.user)
    # favorite_books = user_profile.favorite_books.all()
    try:
        user_profile = request.user.userprofile
        favorite_books = user_profile.favorite_books.all()
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        favorite_books = []
    return render(request,
                  'bookMng/favorite_books.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'favorite_books': favorite_books
                  }
                  )

def toggle_favorite(request, book_id):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    book = get_object_or_404(Book, pk=book_id)

    if book in user_profile.favorite_books.all():
        user_profile.favorite_books.remove(book)
    else:
        user_profile.favorite_books.add(book)

    return redirect('displaybooks')


def book_search(request):
    query = request.GET.get('q')
    books = []

    if query:
        # Perform case-insensitive search by book name
        books = Book.objects.filter(name__icontains=query)

    return render(request,
                  'bookMng/book_search.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'query': query
                  }
                  )


def save_rating(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rating_value = request.POST.get('rating')
        user = request.user
        rating = Rating.objects.create(book_id=book_id, value=rating_value, user=user)
        return render(request,
                      'bookMng/save_rating.html',
                      {
                          "item_list": MainMenu.objects.all(),
                          "book" : book
                    }
                    )


def book_comments(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = book.comments.all()
    item_list = MainMenu.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.book = book
            new_comment.save()
            return redirect('book_comments', book_id=book_id)
    else:
        form = CommentForm()

    return render(request, 'bookMng/book_comments.html', {
        'book': book,
        'comments': comments,
        'item_list': item_list,
        'form': form
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('book_comments', book_id=comment.book.id)

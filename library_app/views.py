from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Book, Reader, Copy, Loan, Author, Publisher, Genre


def reader_list(request):
    """Страница Читатели"""
    readers = Reader.objects.all()
    selected_reader = None
    reader_loans = []

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        readers = readers.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query)
        )

    # Выбор читателя
    reader_id = request.GET.get('select_reader')
    if reader_id:
        selected_reader = get_object_or_404(Reader, id_reader=reader_id)
        reader_loans = Loan.objects.filter(id_reader=selected_reader).select_related('id_copy__id_book')

    # Добавление читателя
    if request.method == 'POST' and 'add_reader' in request.POST:
        Reader.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address')
        )
        return redirect('reader_list')

    # Редактирование читателя
    if request.method == 'POST' and 'edit_reader' in request.POST:
        reader = get_object_or_404(Reader, id_reader=request.POST.get('reader_id'))
        reader.first_name = request.POST.get('first_name')
        reader.last_name = request.POST.get('last_name')
        reader.phone = request.POST.get('phone')
        reader.email = request.POST.get('email')
        reader.address = request.POST.get('address')
        reader.save()
        return redirect(f'/reader_list/?select_reader={reader.id_reader}')

    # Возврат книги
    if request.method == 'POST' and 'return_book' in request.POST:
        loan = get_object_or_404(Loan, id_loan=request.POST.get('loan_id'))
        if not loan.return_date:
            loan.return_date = timezone.now().date()
            if loan.return_date > loan.due_date:
                days_overdue = (loan.return_date - loan.due_date).days
                loan.fine = days_overdue * 10
            loan.save()
            copy = loan.id_copy
            copy.status = 'available'
            copy.save()
        return redirect(f'/reader_list/?select_reader={loan.id_reader.id_reader}')

    context = {
        'readers': readers,
        'selected_reader': selected_reader,
        'reader_loans': reader_loans,
        'search_query': search_query,
    }
    return render(request, 'library_app/reader_list.html', context)


def book_list(request):
    """Страница Книги"""
    books = Book.objects.select_related('id_author', 'id_publisher', 'id_genre').all()
    selected_book = None
    available_copies = []
    readers = Reader.objects.all()

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(title__icontains=search_query)

    # Выбор книги
    book_id = request.GET.get('select_book')
    if book_id:
        selected_book = get_object_or_404(Book, id_book=book_id)
        available_copies = Copy.objects.filter(id_book=selected_book)

    # Добавление книги
    if request.method == 'POST' and 'add_book' in request.POST:
        book = Book.objects.create(
            title=request.POST.get('title'),
            isbn=request.POST.get('isbn'),
            id_author_id=request.POST.get('author_id'),
            id_publisher_id=request.POST.get('publisher_id'),
            id_genre_id=request.POST.get('genre_id')
        )
        Copy.objects.create(id_book=book, status='available')
        return redirect('book_list')

    # Редактирование книги
    if request.method == 'POST' and 'edit_book' in request.POST:
        book = get_object_or_404(Book, id_book=request.POST.get('book_id'))
        book.title = request.POST.get('title')
        book.isbn = request.POST.get('isbn')
        book.id_author_id = request.POST.get('author_id')
        book.id_publisher_id = request.POST.get('publisher_id')
        book.id_genre_id = request.POST.get('genre_id')
        book.save()
        return redirect(f'/book_list/?select_book={book.id_book}')

    # Выдача книги
    if request.method == 'POST' and 'issue_book' in request.POST:
        copy = get_object_or_404(Copy, id_copy=request.POST.get('copy_id'))
        reader = get_object_or_404(Reader, id_reader=request.POST.get('reader_id'))
        if copy.status == 'available':
            due_date = timezone.now().date() + timedelta(days=14)
            Loan.objects.create(
                id_reader=reader,
                id_copy=copy,
                due_date=due_date
            )
            copy.status = 'issued'
            copy.save()
        return redirect(f'/book_list/?select_book={request.POST.get("book_id")}')

    # Изменение статуса экземпляра
    if request.method == 'POST' and 'change_status' in request.POST:
        copy = get_object_or_404(Copy, id_copy=request.POST.get('copy_id'))
        new_status = request.POST.get('status')
        if new_status in ['available', 'issued', 'lost', 'repair']:
            copy.status = new_status
            copy.save()
        return redirect(f'/book_list/?select_book={request.POST.get("book_id")}')

    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    genres = Genre.objects.all()

    context = {
        'books': books,
        'selected_book': selected_book,
        'available_copies': available_copies,
        'readers': readers,
        'authors': authors,
        'publishers': publishers,
        'genres': genres,
        'search_query': search_query,
    }
    return render(request, 'library_app/book_list.html', context)
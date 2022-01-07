from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from core.models import Book, Contact, Categories, Book_request
from django.http import Http404

from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.

def handle_signup(request):
    if request.method == "POST":
        usn = request.POST.get("usn")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        Success = True
        # TODO Validate the data
        usn_exists = User.objects.filter(username=usn).first()
        email_exists = User.objects.filter(email=email).first()
        if usn_exists is not None:
            messages.error(request, "The USN already exists")
            Success=False
        if email_exists is not None:
            messages.error(request, "The Email ID already exists")
            Success=False
        if len(usn)<10:
            messages.error(request, "USN must be atleast 10 characters in length")
            Success=False
        if len(fname)<2:
            messages.error(request, "First Name must atleast contain two characters")
            Success=False
        if len(fname)<1:
            messages.error(request, "Last Name must atleast contain one character")
            Success=False
        if len(email)<4:
            messages.error(request, "Length of Email-id must be greater than 3 characters")
            Success=False
        if len(pass1)<8:
            messages.error(request, "Password must contain atleast 8 characters")
            Success=False
        if pass1 != pass2:
            messages.error(request, "Entered passwords does not matches each other")
            Success=False
        if Success:  
            new_user = User.objects.create_user(usn, email, pass1)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.save()
            # TODO VERIFY USING OTP
            return redirect("/login")
    return render(request, "sign-up.html")


def handle_login(request):
    if request.method == "POST":
        usn = request.POST.get('usn')
        password = request.POST.get('pass')
        user = authenticate(username=usn, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "You have entered wrong USN or Password")
            return render(request, "sign-in.html")
    return render(request, "sign-in.html")


@login_required
def handle_logout(request):
    logout(request=request)
    return redirect("/login")

@login_required
def index(request):
    books = Book.objects.all().exclude(user=request.user)
    requested_books = Book_request.objects.filter(sender=request.user)
    req_books_id = []
    req_books_accepted = []
    for rq_book in requested_books:
        req_books_id.append(rq_book.book.id)
        if(rq_book.accepted):
            req_books_accepted.append(rq_book.book.id)
    return render(request, "index.html", context = {
        "books": books,
        "req_books_id": req_books_id,
        "req_books_accepted": req_books_accepted,
        "req_books": requested_books,
    })


@login_required
def add_book(request):
    # TODO Check the file extension of the uploaded file
    # TODO validate length of title etc
    contact = Contact.objects.filter(rel = request.user).first()
    if contact is None:
        messages.info(request, "Please add the Contact Before adding a Book")
        return redirect("/add_contact")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        edition = request.POST.get('edition')
        desc = request.POST.get('desc')
        thumbnail =request.FILES['thumbnail']
        cat= request.POST.get('cat')
        cat = Categories.objects.filter(id=cat).first()
        print(cat)
        user = request.user
        fs = FileSystemStorage()
        f = fs.save("" + thumbnail.name, thumbnail)       
        book = Book(title=title, author=author, desc=desc,edition=edition,user=user,thumbnail=f, categories=cat)
        book.save()
        messages.success(request, "The Book has been successfully Added")
        return redirect("/my_book")
    cats = Categories.objects.all()
    return render(request, "add-book.html", context={
        "cats": cats,
    })


@login_required
def delete_book(request, id):        
    book = get_object_or_404(Book, id=id)
    if request.user.id is book.user.id:
        book.delete()
        messages.success(request, "You Book has been Deleted Successfully")
    else:
        messages.error(request, "You are Not Authorized to Delete Book of Other Users")
    return redirect("/my_book")


@login_required
def update_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.user.id is not book.user.id:
        messages.error(request, "You are Not Authorized to Update Book of Other Users")
        return redirect("/my_book")
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        edition = request.POST.get('edition')
        desc = request.POST.get('desc')
        user = request.user
        book.title = title
        book.author= author
        book.edition = edition
        book.desc = desc
        book.user = user
        book.save()
        messages.success(request, "Your Book has been Successfully Updated")
        # TODO Change the Thumbnail
        return redirect("/my_book")
    return render(request, "update.html", context={
        "book":book,
    })


@login_required
def my_book(request):
    user = request.user
    books = Book.objects.filter(user=user)
    return render(request, "my_book.html", context={
        "books": books,
    })


@login_required
def search(request):
    # TODO Improve Search Quality
    search_term = request.GET.get('search_text')
    if search_term:
        books = Book.objects.filter(title__icontains = search_term).exclude(user=request.user)
    else:
        books = Book.objects.all()
    return render(request, "search.html", context={'search_term': search_term, 'books': books})


@login_required
def categories(reuqest):
    cats = Categories.objects.all()
    return render(reuqest, "category.html",{
        "categories": cats,
    })
    # TODO Frontend for No Categories 

@login_required
def categories_post(request, id):
    cat =get_object_or_404(Categories,id=id)
    books = Book.objects.filter(categories=cat)
    return render(request, "category_post_list.html",{
        "category": cat,
        "books":books,
    })


@login_required
def add_category(request):
    # TODO Add a parent category
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        cat = Categories(title=title, desc=desc)
        cat.save()
        messages.success(request, "The Category has been Added")
        return redirect("/category")
    return render(request, "add_categories.html")


@login_required
def add_contact(request):
    contact = Contact.objects.filter(rel = request.user).first()
    if contact is not None:
        messages.error(request, "You had added Your contact rather go to update contact")
        return redirect(f"/view_contact/{ request.user.id }")
    if request.method == "POST":
            mob = request.POST.get('mob')
            branch = request.POST.get('branch')
            sem = request.POST.get('sem')
            user = request.user
            contact =  Contact(rel = user, mob = mob, branch=branch, sem=sem)
            contact.save()
            messages.success(request, "Your contact has been added")
            return redirect(f"/view_contact/{request.user.id}")
    return render(request,"add_contact.html")


@login_required
def view_contact(request, user):
    req = Book_request.objects.filter(sender=request.user).filter(accepted=1).first()
    if req is not None or user is request.user.id:
        contact = Contact.objects.filter(rel = user).first()
        if contact is None and user is request.user.id:
            messages.warning(request, "Add Your Contact First")
            return redirect(f"/add_contact")
        elif contact is None:
            messages.warning(request, "The user has not added his contact")
            return redirect("/")
        return render(request, "contact_details.html", context={"contact": contact})
    else:        
        messages.add_message(request, messages.ERROR, "You don't have access to the contact")
        return redirect("/")

@login_required
def update_contact(request, user):
    # TODO return values in the template to display in the form
    # Todo Implement for other details also
    contact = Contact.objects.filter(rel = request.user).first()
    if request.method == 'POST':
        if request.user.id is user:
            mob = request.POST.get('mob')
            branch = request.POST.get('branch')
            sem = request.POST.get('sem')
            user = request.user
            contact.rel = user 
            contact.mob = mob
            contact.branch = branch
            contact.sem = sem 
            contact.save()
            messages.success(request, "Your contact has been Updated")
            return redirect(f"/view_contact/{request.user.id}")
        else:
            messages.error(request,"You can't update contact of other users")
            redirect("/")
    if contact is None:
        messages.warning(request, "You didn't have any contact added, Add a contact Before Updating")
        return redirect("/add_contact") 
    return render(request, "update_contact.html")

@login_required
def book_request(request, id):
    sender = request.user
    book = get_object_or_404(Book, id=id)
    reciever = book.user
    if sender.id is reciever.id:
        messages.warning(request, "You are requesting to your own Book")
        return redirect("/")
    
    if Book_request.objects.filter(sender=sender, reciever=reciever, book=book).first() is not None:
        messages.warning(request, "You can't send multiple request to the same book")
        return redirect("/")

    req = Book_request(sender=sender, reciever=reciever, accepted=False, rejected=False, book=book)
    req.save()
    messages.add_message(request, messages.INFO, "The Book Request has been send")
    return redirect("/")


@login_required
def accept_request(request, id):
    req = get_object_or_404(Book_request, id=id)
    if request.user.id is req.reciever.id:
        req.accepted=True;
        req.rejected=False;
        req.save()
        messages.success(request, "The request has been Accepted")
    else:
        messages.error(request, "You can't Accept Book Request of Books You don't Owned")
    return redirect("/")


@login_required
def reject_request(request, id):
    req = get_object_or_404(Book_request, id=id)
    if request.user.id is req.reciever.id:
        req.delete() 
        messages.success(request, "The request has been rejected")
    else:
        messages.error(request, "You can't reject Book Request of Book you don't Owned")
    return redirect("/")
        

def custom_404(request, exception):    
    return render(request, "404.html", status=404)
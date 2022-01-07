from core.models import Book_request

def all_request(request):
    if request.user.is_authenticated:
        reqs = Book_request.objects.filter(reciever=request.user).filter(accepted=False)
        count = reqs.__len__()
        return {
            "all_request": reqs,
            "count": count,
        }
    else:
        return {}
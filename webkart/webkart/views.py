from django.shortcuts import redirect

# index
def index(request):
    return redirect('shop:home')
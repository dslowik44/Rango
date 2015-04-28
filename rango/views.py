from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):  
   category_list = Category.objects.order_by('-likes')[:5]
   context_dict = {'categories': category_list}
   top_pages_list = Page.objects.order_by('-views')[:5]
   context_dict['top_pages'] = top_pages_list
   return render(request, 'rango/index.html', context_dict)
	
def category(request, category_name_slug):
    context_dict = {}	
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category'] = category
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist: #get() gets single category or raises Category.DoesNotExist.
        pass
	
    return render(request, 'rango/category.html', context_dict)

@login_required	
def add_category(request):
#    import pdb
#    pdb.set_trace()
    if request.method == 'POST':
       form = CategoryForm(request.POST)			
       if form.is_valid():
          form.save(commit=True)	
          return HttpResponseRedirect('/rango/')  # vs. index(request)
       else:
          print form.errors
    else:
       form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
       cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
       cat = None
	
    if request.method == 'POST':
       form = PageForm(request.POST)	
       if form.is_valid():		
          if cat:
             page = form.save(commit=False)	
             page.category = cat
             page.views = 0
             page.save()
             return HttpResponseRedirect('/rango/')  # vs. index(request)
       else:
          print form.errors
    else:
       form = PageForm()
	   
    context_dict = {'form':form, 'category':cat, 'slug':category_name_slug}

    return render(request, 'rango/add_page.html/', context_dict)

def register(request):
    if request.method == 'POST':
       user_form = UserForm(request.POST)			
       profile_form = UserProfileForm(request.POST)
       if user_form.is_valid() and profile_form.is_valid():
          user = user_form.save(commit=False)
          user.set_password(user.password)
          user.save()
          profile = profile_form.save(commit=False)
          profile.user = user
          if 'picture' in request.FILES:
              profile.picture = request.FILES['picture']
          profile.save()
          return HttpResponseRedirect('/rango/reg_success/')
       else:
          print user_form.errors, profile_form.errors
    else:
       user_form = UserForm()
       profile_form = UserProfileForm
    registered = True
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form':profile_form,
												   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            if user.is_active: #check acct not dissabled.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.") #dangling..
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")     #dangling..

    else:
       return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


def about(request):
    context_dict = {'boldmessage': "here is the about page."}
    return render(request, 'rango/about.html', context_dict)



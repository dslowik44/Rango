from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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
	
def about(request):
	context_dict = {'boldmessage': "here is the about page."}
	return render(request, 'rango/about.html', context_dict)
	
   

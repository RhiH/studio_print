from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import ArtistsCategory, ArtistsInfo

# Create your views here.


def all_artists(request):
    """ A view to show all artists"""

    artists = Artists.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                artists = artists.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            artists = artists.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search query")
                return redirect(reverse('artists'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    
    current_sorting = f'{sort}_{direction}'

    context = {
        'artists': artists,
        'search_term': query,
        'current_artists': artists,
        'current_sorting': current_sorting,
    }

    return render(request, 'artists/artists.html', context)


def artists_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'artist': artist,
    }

    return render(request, 'artists/artist_detail.html', context)


def artists_about_us(request):
    """ A view to show iabout the site """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'artist': artist,
    }

    return render(request, 'artists/artist_detail.html', context)

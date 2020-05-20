from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Movie, Genre

# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.like_movies:
        user_movies = request.user.like_movies.all()
        genres_dic = {}
        for movie in user_movies:
            for genre in movie.genres.all():
                if genre.name in genres_dic:
                    genres_dic[genre.id] += 1
                else:
                    genres_dic[genre.id] = 1
        genres_sort = sorted(genres_dic.items(), key=lambda x:x[1], reverse=True)
        print(genres_sort)
        most_liked_genre = genres_sort[0][0]
        print(most_liked_genre)
        recommend_movies = []
        for movie in Movie.objects.order_by('-popularity'):
            for genre in movie.genres.all():
                # print(genre)
                if most_liked_genre == genre.id:
                    recommend_movies.append(movie)
                    if len(recommend_movies)==10:
                        break
            if len(recommend_movies)==10:
                break
    else:
        recommend_movies = Movie.objects.order_by('-popularity')[:10]
    movies = Movie.objects.order_by('-vote_average')
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'recommend_movies' : recommend_movies,
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)

@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    return JsonResponse({
        'liked' : liked,
        'like_count' : movie.like_users.count(),
    })


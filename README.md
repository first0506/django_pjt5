# README

### 어려웠던 점

1. JSON 형식 파일 Load
   * 처음 모델링을 했을 때 json  파일의 필드명과 다르게 필드명을 지어서 로드하는데 어려움을 겪었습니다.



2. 10개의 영화 추천 알고리즘

   ```python
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
   ```

   Movie 모델의 genres 속성을 가져올 때, 하나의 genre만 가져오는 것이 아니라 M:N 관계이기 때문에 모든 genre를 가지고 왔습니다. 이를 헷갈려서 한 movie 객체의 genre를 가져오는데 시간을 많이 소비했습니다.



### 추천 알고리즘

- 이번 페어 프로젝트에서 사용한 추천 알고리즘은 사용자가 좋아요를 가장 많이 한 장르를 구하고, 그 장르의 영화를 popularity 순으로 내림차순하여 10개를 뽑았습니다.
- 만약 사용자가 로그인 하지 않은 상태에서는 모든 영화를 popularity 순으로 내림차순하여 10개를 뽑았습니다.



### 느낀점

*  이제껏 진행한 페어 프로젝트 중 가장 많은 어려움이 있었고, 시간도 많이 걸렸습니다. 하지만 페어와 같이 문제를 해결해가면서 더 많은 것은 배울 수 있었고, 보람도 더욱 많이 느껴졌습니다.


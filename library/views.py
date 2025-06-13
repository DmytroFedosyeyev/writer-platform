from django.shortcuts import render, redirect, get_object_or_404
from .models import Work, Rating
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import RatingForm, CommentForm
from django.db.models import Avg



class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'genre', 'content']


@login_required
def create_work_view(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.author = request.user
            work.save()
            return redirect('work_list')
    else:
        form = WorkForm()
    return render(request, 'library/create_work.html', {'form': form})


@login_required
def work_detail_view(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    comments = work.comments.all().order_by('-created_at')

    # Получаем оценку пользователя (если уже оценивал)
    user_rating = Rating.objects.filter(user=request.user, work=work).first()

    if request.method == 'POST':
        if 'rate_submit' in request.POST:
            rating_form = RatingForm(request.POST, instance=user_rating)
            comment_form = CommentForm()
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.work = work
                rating.save()
                return redirect('work_detail', work_id=work.id)
        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            rating_form = RatingForm(instance=user_rating)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.work = work
                comment.save()
                return redirect('work_detail', work_id=work.id)
    else:
        rating_form = RatingForm(instance=user_rating)
        comment_form = CommentForm()

    # Средняя оценка
    average_rating = work.ratings.aggregate(Avg('score'))['score__avg']

    return render(request, 'library/work_detail.html', {
        'work': work,
        'comments': comments,
        'form': comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'user_rating': user_rating,
    })


@login_required
def work_list_view(request):
    title_query = request.GET.get('title', '')
    genre_filter = request.GET.get('genre', '')
    author_query = request.GET.get('author', '')

    works = Work.objects.none()  # По умолчанию пустой список

    # Если есть хотя бы один фильтр, применяем фильтрацию
    if title_query or genre_filter or author_query:
        works = Work.objects.all().order_by('-published_date')

        if title_query:
            works = works.filter(title__icontains=title_query)

        if genre_filter:
            works = works.filter(genre=genre_filter)

        if author_query:
            works = works.filter(author__username__icontains=author_query)

    return render(request, 'library/work_list.html', {
        'works': works,
        'title_query': title_query,
        'genre_filter': genre_filter,
        'author_query': author_query,
        'work_model': Work,
    })
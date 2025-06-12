from django.shortcuts import render, redirect, get_object_or_404
from .models import Work
from django.contrib.auth.decorators import login_required
from django import forms


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
    return render(request, 'library/work_detail.html', {'work': work})


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
    })
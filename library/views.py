import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from .models import Work, Rating
from django.contrib.auth.decorators import login_required
from .forms import RatingForm, CommentForm, WorkForm
from django.db.models import Avg, Count, Case, When, IntegerField, Q
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

# Настройка логгера
logger = logging.getLogger('library')

@login_required
def create_work_view(request):
    logger.info("Запрос на создание нового произведения")
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.author = request.user
            work.save()
            logger.info(f"Произведение '{work.title}' успешно создано пользователем {request.user.username}")
            return redirect('work_list')
        else:
            logger.error(f"Ошибка валидации формы создания произведения: {form.errors}")
    else:
        form = WorkForm()
    return render(request, 'library/create_work.html', {'form': form})

def work_detail_view(request, work_id):
    logger.info(f"Запрос на просмотр произведения с ID {work_id}")
    work = get_object_or_404(Work, id=work_id)
    comments = work.comments.all().order_by('-created_at')

    rating_form = None
    comment_form = None
    show_auth_message = not request.user.is_authenticated
    user_rating = None
    has_rated = False

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, work=work).first()
        has_rated = user_rating is not None
        rating_form = RatingForm(instance=user_rating) if not has_rated else None
        comment_form = CommentForm()

        if request.method == 'POST' and not has_rated:
            if 'rate_submit' in request.POST:
                rating_form = RatingForm(request.POST, instance=user_rating)
                if rating_form.is_valid():
                    rating = rating_form.save(commit=False)
                    rating.user = request.user
                    rating.work = work
                    rating.save()
                    logger.info(f"Пользователь {request.user.username} оценил произведение {work.title} на {rating.score}")
                    return redirect('work_detail', work_id=work.id)
                else:
                    logger.error(f"Ошибка валидации формы рейтинга: {rating_form.errors}")
            elif 'comment_submit' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = request.user
                    comment.work = work
                    comment.save()
                    logger.info(f"Пользователь {request.user.username} оставил комментарий к {work.title}")
                    return redirect('work_detail', work_id=work.id)
                else:
                    logger.error(f"Ошибка валидации формы комментария: {comment_form.errors}")

    average_rating = work.ratings.aggregate(Avg('score'))['score__avg']

    words = work.content.split()
    words_per_page = 200
    total_words = len(words)
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1

    total_pages = (total_words + words_per_page - 1) // words_per_page
    page_number = max(1, min(page_number, total_pages))

    start_idx = (page_number - 1) * words_per_page
    end_idx = min(start_idx + words_per_page, total_words)
    while end_idx < total_words and not words[end_idx-1].endswith(' '):
        end_idx += 1
    content_words = words[start_idx:end_idx]
    content = ' '.join(content_words)

    return render(request, 'library/work_detail.html', {
        'work': work,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'user_rating': user_rating,
        'show_auth_message': show_auth_message,
        'content': content,
        'has_rated': has_rated,
        'page_number': page_number,
        'total_pages': total_pages,
    })

#@login_required
def work_list_view(request):
    logger.info("Запрос на список произведений с фильтрами")

    title_query = request.GET.get('title', '')
    genre_filter = request.GET.get('genre', '')
    author_query = request.GET.get('author', '')
    nickname_query = request.GET.get('nickname', '')

    works = Work.objects.all().order_by('-published_date')

    if title_query:
        works = works.filter(title__icontains=title_query)
        logger.info(f"Применён фильтр по названию: {title_query}")

    if genre_filter:
        works = works.filter(genre=genre_filter)
        logger.info(f"Применён фильтр по жанру: {genre_filter}")

    if author_query:
        works = works.filter(
            Q(author__first_name__icontains=author_query) |
            Q(author__last_name__icontains=author_query)
        )
        logger.info(f"Применён фильтр по имени/фамилии автора: {author_query}")

    if nickname_query:
        works = works.filter(author__username__icontains=nickname_query)
        logger.info(f"Применён фильтр по нику автора: {nickname_query}")

    paginator = Paginator(works, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/work_list.html', {
        'works': page_obj,
        'title_query': title_query,
        'genre_filter': genre_filter,
        'author_query': author_query,
        'nickname_query': nickname_query,
        'work_model': Work,
    })

@login_required
def export_work_pdf(request, work_id):
    logger.info(f"Запрос на экспорт PDF для произведения с ID {work_id}")
    work = get_object_or_404(Work, id=work_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{work.title}.pdf"'

    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    p = canvas.Canvas(response)
    y = 800

    p.setFont("DejaVuSans", 16)
    p.drawString(100, y, work.title)
    y -= 30

    p.setFont("DejaVuSans", 12)
    p.drawString(100, y, f"Автор: {work.author.username}")
    y -= 20
    p.drawString(100, y, f"Жанр: {work.get_genre_display()}")
    y -= 20
    p.drawString(100, y, f"Дата публикации: {work.published_date.strftime('%d.%m.%Y %H:%M')}")
    y -= 40

    content_lines = work.content.split('\n')
    for line in content_lines:
        if y < 50:
            p.showPage()
            p.setFont("DejaVuSans", 12)
            y = 800
        p.drawString(100, y, line.strip())
        y -= 20

    p.showPage()
    p.save()
    logger.info(f"PDF для произведения '{work.title}' успешно экспортирован")
    return response

def home_view(request):
    logger.info("Запрос на главную страницу")
    latest_works = Work.objects.all().order_by('-published_date')[:5]
    return render(request, 'home.html', {'latest_works': latest_works})

@login_required
def edit_work_view(request, work_id):
    logger.info(f"Запрос на редактирование произведения с ID {work_id}")
    work = get_object_or_404(Work, id=work_id, author=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            logger.info(f"Произведение '{work.title}' успешно отредактировано пользователем {request.user.username}")
            return redirect('work_detail', work_id=work.id)
        else:
            logger.error(f"Ошибка валидации формы редактирования: {form.errors}")
    else:
        form = WorkForm(instance=work)
    return render(request, 'library/edit_work.html', {'form': form})

class WorkDeleteView(DeleteView):
    model = Work
    template_name = 'library/work_confirm_delete.html'
    success_url = reverse_lazy('work_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            logger.error(f"Пользователь {self.request.user.username} попытался удалить чужое произведение {obj.title}")
            raise PermissionDenied("У вас нет прав для удаления этого произведения.")
        logger.info(f"Пользователь {self.request.user.username} запросил удаление произведения {obj.title}")
        return obj

@login_required
def top_works_view(request):
    logger.info("Запрос на топ-50 произведений")
    sort_by = request.GET.get('sort', 'rating')

    genre_order = ['Другое', 'История', 'Фантастика', 'Поэзия', 'Детектив', 'Триллер', 'Драма']
    display_to_code = {display: code for code, display in Work.GENRE_CHOICES}

    genre_cases = [
        When(genre=display_to_code[name], then=idx)
        for idx, name in enumerate(genre_order)
        if name in display_to_code
    ]
    custom_order = Case(*genre_cases, default=len(genre_order), output_field=IntegerField())

    works = Work.objects.annotate(
        avg_rating=Avg('ratings__score'),
        comment_count=Count('comments'),
        genre_order=custom_order
    )

    if sort_by == 'genre':
        works = works.order_by('genre_order', '-avg_rating')
    elif sort_by == 'rating':
        works = works.order_by('-avg_rating', '-comment_count')
    elif sort_by == 'comments':
        works = works.order_by('-comment_count', '-avg_rating')

    works = works[:50]

    return render(request, 'library/top_works.html', {
        'works': works,
        'sort_by': sort_by,
        'genres': Work.GENRE_CHOICES,
    })

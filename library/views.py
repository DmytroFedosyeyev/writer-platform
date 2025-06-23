from django.shortcuts import render, redirect, get_object_or_404
from .models import Work, Rating
from django.contrib.auth.decorators import login_required
from .forms import RatingForm, CommentForm, WorkForm  # Импортируем WorkForm отсюда
from django.db.models import Avg
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


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

def work_detail_view(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    comments = work.comments.all().order_by('-created_at')

    # Инициализация форм и данных
    rating_form = None
    comment_form = None
    show_auth_message = not request.user.is_authenticated
    user_rating = None
    has_rated = False

    if request.user.is_authenticated:
        # Проверяем, оценивал ли пользователь
        user_rating = Rating.objects.filter(user=request.user, work=work).first()
        has_rated = user_rating is not None

        # Инициализация форм для авторизованных пользователей
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
                    return redirect('work_detail', work_id=work.id)
            elif 'comment_submit' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = request.user
                    comment.work = work
                    comment.save()
                    return redirect('work_detail', work_id=work.id)
                else:
                    print(comment_form.errors)

    # Средняя оценка
    average_rating = work.ratings.aggregate(Avg('score'))['score__avg']

    # Убираем пагинацию текста, передаём весь контент
    return render(request, 'library/work_detail.html', {
        'work': work,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'user_rating': user_rating,
        'show_auth_message': show_auth_message,
        'content': work.content,  # Передаём весь текст без пагинации
        'has_rated': has_rated,
    })

#@login_required
def work_list_view(request):
    title_query = request.GET.get('title', '')
    genre_filter = request.GET.get('genre', '')
    author_query = request.GET.get('author', '')

    # Базовый набор — все работы, если фильтры пустые
    works = Work.objects.all().order_by('-published_date')

    # Применяем фильтры, если они заданы
    if title_query:
        works = works.filter(title__icontains=title_query)

    if genre_filter:
        works = works.filter(genre=genre_filter)

    if author_query:
        works = works.filter(author__username__icontains=author_query)

    # Пагинация
    paginator = Paginator(works, 5)  # 5 работ на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/work_list.html', {
        'works': page_obj,
        'title_query': title_query,
        'genre_filter': genre_filter,
        'author_query': author_query,
        'work_model': Work,
    })

@login_required
def export_work_pdf(request, work_id):
    work = get_object_or_404(Work, id=work_id)

    # Создаём HTTP-ответ как PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{work.title}.pdf"'

    # Регистрируем шрифт с поддержкой кириллицы
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    # Начинаем PDF-документ
    p = canvas.Canvas(response)
    y = 800  # начальная координата

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

    # Контент произведения — построчно
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
    return response

def home_view(request):
    latest_works = Work.objects.all().order_by('-published_date')[:5]
    return render(request, 'home.html', {'latest_works': latest_works})

@login_required
def edit_work_view(request, work_id):
    work = get_object_or_404(Work, id=work_id, author=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('work_detail', work_id=work.id)
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
            raise PermissionDenied("У вас нет прав для удаления этого произведения.")
        return obj
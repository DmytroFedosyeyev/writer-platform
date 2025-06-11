from django.shortcuts import render, redirect
from .models import Work
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import get_object_or_404


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
def work_list_view(request):
    works = Work.objects.all().order_by('-published_date')
    return render(request, 'library/work_list.html', {'works': works})


@login_required
def work_detail_view(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    return render(request, 'library/work_detail.html', {'work': work})
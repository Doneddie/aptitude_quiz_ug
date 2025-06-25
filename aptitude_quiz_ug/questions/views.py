from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import Question, QuizResult
from django.http import Http404
from django.contrib.auth.decorators import login_required

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})

def start_quiz(request, category):
    request.session['quiz_category'] = category
    request.session['quiz_score'] = 0
    request.session['quiz_index'] = 0

    questions = list(Question.objects.filter(category=category).values_list('id', flat=True))
    request.session['quiz_questions'] = questions
    return redirect('take_quiz')

def take_quiz(request):
    questions = request.session.get('quiz_questions', [])
    index = request.session.get('quiz_index', 0)

    if index >= len(questions):
        return redirect('quiz_result')

    question_id = questions[index]
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question not found")

    if request.method == 'POST':
        selected = request.POST.get('option')
        if selected == question.correct_option:
            request.session['quiz_score'] += 1
        request.session['quiz_index'] += 1
        return redirect('take_quiz')

    return render(request, 'questions/take_quiz.html', {'question': question, 'index': index + 1, 'total': len(questions)})

@login_required
def quiz_result(request):
    score = request.session.get('quiz_score', 0)
    total = len(request.session.get('quiz_questions', []))
    category = request.session.get('quiz_category', 'unknown')

    if request.user.is_authenticated:
        QuizResult.objects.create(
            user=request.user,
            category=category,
            score=score,
            total=total
        )

    percentage = int((score / total) * 100) if total > 0 else 0
    return render(request, 'questions/quiz_result.html', {'score': score, 'total': total, 'percentage': percentage})

@login_required
def user_dashboard(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
    return render(request, 'questions/dashboard.html', {'results': results})





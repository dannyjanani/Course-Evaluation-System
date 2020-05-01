from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime


def index(request):
    request.session.flush()
    return render(request, 'eval/index.html', {})

def check_eval_pswd(request):
    eval_pswd = request.POST.get("eval-password", 'blank-pswd')
    now = timezone.now()
    session = EvalSession.objects.filter(session_start__lte = now, session_end__gte = now).first()
    if session is None:
        return render(request, 'eval/index.html', {
            'error_message' : "There is currently no class to evaluate",
        })

    if eval_pswd != session.session_eval_pswd:
        return render(request, 'eval/index.html', {
            'error_message' : "Incorrect password",
        })

    request.session['session_id'] = session.pk
    return redirect('/eval-page')


def eval_page(request):
    now = timezone.now()
    session = EvalSession.objects.filter(session_start__lte = now, session_end__gte = now).first()
    return render(request, 'eval/eval-page.html', {
        'session' : session,
    })


def eval_submit(request):
    # Save evaluation to database, make sure they ticked metric, return them if they didnt, etc.

    metric = request.POST.get('class-metric', '')
    comment = request.POST.get('class-comment', '')

    # If no metric ticked, return to eval page with error message
    if not metric:
        return render(request, 'eval/eval-page.html', {
            'error_message' : "You must tick a class metric for your response to be submitted.",
        })

    # If too late to submit (ex. page was open till after session expiration)
    session = EvalSession.objects.get(pk=request.session['session_id'])
    if not session.is_current_session():
        return render(request, 'eval/after-eval.html', {
            'able_to_submit' : False,
        })

    # If all good
    evaluation = Evaluation(eval_session_id=session, class_metric=metric, class_comment=comment)
    evaluation.save()
    return render(request, 'eval/after-eval.html', {
        'able_to_submit' : True,
    })

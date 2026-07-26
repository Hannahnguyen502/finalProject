from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


# Course Detail View
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


# Task 5 Requirement: submit function
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Verify user enrollment
    enrollment, created = Enrollment.objects.get_or_create(
        user=user, 
        course=course,
        defaults={'mode': Enrollment.AUDIT}
    )

    if request.method == 'POST':
        # Create a new submission instance
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Collect submitted choice IDs from POST request
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))

        # Add choices to submission
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)

        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    return redirect('onlinecourse:course_details', course_id=course.id)


# Task 5 Requirement: show_exam_result function
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    total_score = 0
    max_score = 0
    selected_ids = [choice.id for choice in submission.choices.all()]

    # Calculate total exam score
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            max_score += question.grade
            if question.is_get_score(selected_ids):
                total_score += question.grade

    grade = (total_score / max_score * 100) if max_score > 0 else 0

    context['course'] = course
    context['selected_ids'] = selected_ids
    context['total_score'] = total_score
    context['max_score'] = max_score
    context['grade'] = grade

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
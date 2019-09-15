from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, authenticate
from .forms import CourseEnrollForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from django.views.generic.base import View


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    success_url = ('student_course_list')
    form_class = UserCreationForm  #the form for creating objects which has to be modelform

    # this function is executed when valid form data has being posted.
    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data  # submitted data

        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)  # login user to the current session.
        return result

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self)\
            .form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:student_course_detail',
                            args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        """Retrieve courses enrolled by the current.
        student in the session."""
        qs = super(StudentCourseListView, self) \
                .get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self) \
                .get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self) \
                    .get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            #get first module
            context['module'] = course.modules.all()[0]

        return context

from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from .permissions import IsEnrolled

# list and detail view to retrieve objects
class SubjectListView(generics.ListAPIView):
    """This view will retrieve all objects."""
    queryset = Subject.objects.all()  # all subject objects
    serializer_class = SubjectSerializer  # fields to be serialized

class SubjectDetailView(generics.RetrieveAPIView):
    """This view will retrieve the details of a particular
    subject object by passing its pk in its url."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# class CourseEnrollView(APIView):
#     # this view only recieves post requests
#     # authentication identifies the user and set him as request.user or anonymousUser
#     # it doesn't prevent the user from accessing the view for that we need permissions.
#     authentication_classes = (BasicAuthentication,)
#     # only authenticated users are allowed to access this view.
#     permission_classes = (IsAuthenticated,)  
#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled':True})

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Provide read-only actions list() and retrieve().
    to list objects or retrieve a single course object."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['post'],
                    authentication_classes=(BasicAuthentication,),
                    permission_classes=(IsAuthenticated,))
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled':True})

    @detail_route(methods=['get'],
                    serializer_class=CourseWithContentSerializer,
                    authentication_classes=(BasicAuthentication,),
                    permission_classes=(IsAuthenticated, IsEnrolled))
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
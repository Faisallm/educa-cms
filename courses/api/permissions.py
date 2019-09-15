# we are creating custom permissions so that 
# students that have enrolled on a particular course
# are the only ones accessing its contents.

from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    # in this case obj refers to course
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()  # returns a boolean. 
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# we are creating a custom model field called order
# it should automatically provide an order value when none is provided
# course modules should be ordered according to the course the belong to
# modules contents should be ordered according to the module the belong to
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields  # we want to order the module to the course it belongs to
        super(OrderField, self).__init__(*args, **kwargs)

    # getattr(object, name)
    # setattr(object, name, value)
    def pre_save(self, model_instance, add):    
        if getattr(model_instance, self.attname) is None:
            # getattr(module, 'object') is None (id no  value is provided) or
            # getattr(content, 'objects') is None
            # no value has being provided for order.
            try:
                qs = self.model.objects.all()  # retrieve all objects from the field model
                # eg Module.objects.all() or Content.objects.all()
                if self.for_fields:
                    # retrieve the course or module the module or content belong to respectively
                    # getattr(module, 'course')
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    # filter modules belonging to this particular course
                    qs = qs.filter(**query)  

                # get last module
                last_item = qs.latest(self.attname)
                # increment module order by one
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            # setattr(object, name, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)        
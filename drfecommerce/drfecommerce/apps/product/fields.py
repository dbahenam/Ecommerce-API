from django.db import models
from django.core.checks import Error
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    description = ("An ordering field that ensures order values are unique "
               "relative to another specified field in the model.")

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        field_names = [f.name for f in self.model._meta.get_fields()]

        # Ensure unique_for_field is set properly
        if not self.unique_for_field:
            errors.append(
                Error(
                    "'unique_for_field' attribute must be set.",
                    hint="Set the 'unique_for_field' attribute to a field name within the model.",
                    obj=self,
                    )
            )
        elif self.unique_for_field not in field_names:
            errors.append(
                Error(
                    f"'{self.unique_for_field}' field does not exist in the model.",
                    hint=f"Ensure that '{self.unique_for_field}' is a valid field name within the model.",
                    obj=self,
                )
            )
        return errors

    def pre_save(self, model_instance, add):
        # getattr returns value of named attribute
        qs = self.model.objects.all() # get all objects, e.g product line
        print("self.attname: ", self.attname)
        print("model instance: ", model_instance)
        print("unique for field: ", self.unique_for_field)
        print("getattr: ", getattr(model_instance, self.unique_for_field))
        
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all() # get all objects, e.g product line
            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(**query)
                last_obj = qs.latest(self.attname)
                value = last_obj.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)
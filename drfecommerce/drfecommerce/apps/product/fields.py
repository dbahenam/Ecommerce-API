from django.db import models
from django.core.checks import Error
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = (
        "An ordering field that determines order based on the latest value held "
        "for a group of objects sharing the same attribute defined in 'unique_for_field'. "
        "Uniqueness should be ensured by the model using this field."
    )

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        field_names = [f.name for f in self.model._meta.get_fields()]

        # Ensure unique_for_field is set and also set to a field within the model
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
        # getattr returns value of named attribute, ex getattr(Product, product_obj) -> product.name
        # ex: model_instance=product_line, name=product --> getattr(product_line.product) = 'kobes'
        qs = self.model.objects.all()  # get all objects, e.g from product line

        if getattr(model_instance, self.attname) is None:  # self.attname = order
            qs = self.model.objects.all()  # get all objects, e.g product line
            try:
                query = {  # {Product: kobes}
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(
                    **query
                )  # qs.filter(product=kobes), get productline objects where product=kobes
                last_obj = qs.latest(self.attname)  # get object with latest order
                value = last_obj.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)

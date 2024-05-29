from django.core.checks import CheckMessage
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    description = "Ordering field on unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)
    
    def check(self, **kwargs):
        return[
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]
    
    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("orderfield must define a 'unique_for_forld' attribute")
                ]
        elif self.unique_for_field not in  [f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error(
                    "orderField entered does not match an existing model field"
                )
                ]
        return []
    

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            qs= self.model.objects.all()
            try:
                query = {(
                    self.unique_for_field
                )}
                qs=qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)
        
        
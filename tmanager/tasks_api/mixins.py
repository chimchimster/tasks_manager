from rest_framework.exceptions import ValidationError


class CommonValidationMixin:

    model = None

    def validate(self, attrs: dict):
        instance = self.model
        try:
            instance.clean_fields()
        except ValidationError as v:
            raise ValidationError(v.detail)

        return attrs

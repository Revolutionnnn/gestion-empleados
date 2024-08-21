from rest_framework.exceptions import ValidationError


class ProtectRelatedDeleteMixin:
    """
    Mixin to prevent deletion if there are related objects.
    """
    def perform_destroy(self, instance):
        related_objects = self.get_related_objects(instance)
        for related_object in related_objects:
            if related_object.exists():
                raise ValidationError(f'No puedes eliminar esta informacion esta relacionada con otra informacion.')
        super().perform_destroy(instance)

    def get_related_objects(self, instance):
        """
        Returns a list of related objects for the given instance.
        """
        related_objects = []
        for related_field in instance._meta.related_objects:
            related_manager = getattr(instance, related_field.get_accessor_name())
            related_objects.append(related_manager.all())
        return related_objects

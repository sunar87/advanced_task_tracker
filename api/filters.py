import django_filters
from tasks.models import Task
from tasks.const import STATUS_CHOICES, PRIORITY_CHOICES


class TaskFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name='tags__name',
        lookup_expr='icontains'
        )
    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES
        )
    priority = django_filters.ChoiceFilter(
        choices=PRIORITY_CHOICES
        )

    class Meta:
        model = Task
        fields = ['tags', 'status', 'priority']

import uuid
from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:department', args=[self.slug])


def program_file_path(instance, file):
    return f'data/{instance.year}/{instance.department}/{file}'


class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.CharField(verbose_name='program or project name', max_length=150,)
    slug = models.SlugField(max_length=200, db_index=True)
    department = models.ForeignKey(Department, max_length=150, related_name='programs',  on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    # file = models.FileField(upload_to='data/year/department/program/', blank=False)
    file = models.FileField(upload_to=program_file_path, blank=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_uploaded',)
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.program

    def get_absolute_url(self):
        return reverse('main:program_detail', args=[self.id, self.slug])

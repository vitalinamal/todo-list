from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, blank=True, null=True, related_name="tags")

    class Meta:
        ordering = ["completed", "-created_at"]

    def __str__(self):
        return self.content

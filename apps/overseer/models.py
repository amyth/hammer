from django.db import models


class String(models.Model):
    """
    Represents a string model. This is a the base model, all
    other models that represent a string should extend this
    model.
    """

    content = models.CharField(max_length=244)
    children = models.ManyToManyField('self')
    normalized_id = models.IntegerField(blank=True, null=True)
    is_parent = models.BooleanField(default=False)
    is_normalized = models.BooleanField(default=False)
    is_abbreviation = models.BooleanField(default=False)


class Match(models.Model):
    """
    Represents a match object between two string objects.
    """

    string_one = models.ForeignKey(String, related_name='string_one_set')
    string_two = models.ForeignKey(String, related_name='string_two_set')
    match_percentile = models.IntegerField(default=0)


class Institute(String):
    """
    Represents a institute name
    """
    pass

from celery import Task

from django.conf import settings
from django.db.models import Q

from apps.overseer import models

from lib import hammerlib, utils


class CreateBulkInstitutes(Task):
    """
    Creates institute objects based on the given json data.
    """

    def run(self, data, *args, **kwargs):
        """
        For each entry found in data, we try creating a new
        institute object.
        """

        for obj in data:
            name = obj.get('inc')
            normalized_id = obj.get('ins')
            exists = models.Institute.objects.filter(content=name).exists()
            if not exists:
                try:
                    if normalized_id:
                        models.Institute.objects.create(
                                content=name,
                                normalized_id=normalized_id,
                                is_normalized=True,
                                is_parent=True)
                    else:
                        models.Institute.objects.create(
                            content=name)
                except Exception as err:
                    #TODO: Log the error once logging is in place.
                    ##     See T5 for more information.
                    print "Could not create institute: %s, data: %s" % (
                            str(err), obj)


class UpdateMatches(Task):
    """
    Updates matches if any unprocessed string is present in
    the database
    """

    def run(self, *args, **kwargs):

        to_process = models.Institute.objects.filter(
                    is_normalized = False,
                    is_processed = False)

        all_institutes = models.Institute.objects.all()

        for x in to_process:
            xcon = utils.clean_string(x.content)
            for y in all_institutes:
                ycon = utils.clean_string(y.content)

                if not (x == y):
                    match_percent = hammerlib.spellmatch(xcon, ycon)

                    if match_percent > settings.MINMATCH_PERCENT:
                        m = models.Match.objects.filter(Q(
                            string_two = x, string_one = y) | Q(
                            string_two = y, string_one = x))

                        if not m.exists():
                            models.Match.objects.create(
                                string_one = x,
                                string_two = y,
                                match_percentile = match_percent)

            x.is_processed = True
            x.save()
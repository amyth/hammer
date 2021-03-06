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
            
            inst_type = models.InstituteType.objects.get(id = 1)

            models.NormalizedInstitute.objects.create(
                name = obj.get('name'),
                city = obj.get('location.city','None'),
                state = obj.get('location.state','None'),
                country = obj.get('location.country','None'),
                established = obj.get('established',0),
                type_of_institute = inst_type)


class CreateMatches(Task):
    """
    Creates match objects based on the given json data.
    """

    def run(self, data, *args, **kwargs):
        """
        For each entry found in data, we try creating a new
        match object.
        """

        for obj in data:

            s = obj.get('inc')

            new_unnorm = models.UnnormalizedInstitute.objects.filter(name = s)

            if not new_unnorm:
                models.UnnormalizedInstitute.objects.create(
                    name = s)
            else:
                u = models.UnnormalizedInstitute.objects.get(name = s)
                u.frequency = u.frequency + 1
                u.save()

        all_unnormalized = models.UnnormalizedInstitute.objects.all()
        all_normalized = models.NormalizedInstitute.objects.all()

        for y in all_normalized:
        
            y_name = utils.clean_string(y.name)
            
            for x in all_unnormalized:
                x_name = utils.clean_string(x.name)    
                match_percent = hammerlib.spellmatch(x_name, y_name)

                if match_percent > settings.MINMATCH_PERCENT:
                    m = models.InstituteMatches.objects.filter(
                        normalized_inst__pk = y.pk, unnormalized_inst__pk = x.pk)

                    if not m.exists():
                        models.InstituteMatches.objects.create(
                            normalized_inst = y,
                            unnormalized_inst = x,
                            match_score = match_percent,
                            status = 1)

                        unnorm_ins = models.UnnormalizedInstitute.objects.get(pk = x.pk)
                        unnorm_ins.no_of_matches = unnorm_ins.no_of_matches + 1
                        unnorm_ins.status = 1
                        unnorm_ins.save()

                        normalized_ins = models.NormalizedInstitute.objects.get(pk = y.pk)
                        normalized_ins.no_of_matches = normalized_ins.no_of_matches + 1
                        normalized_ins.cummulative_matches = normalized_ins.cummulative_matches + unnorm_ins.frequency
                        normalized_ins.save()

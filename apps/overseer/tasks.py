from celery import Task

from apps.overseer import models


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

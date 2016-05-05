from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

class NormalizedInstitute(models.Model):

    name = models.CharField(max_length=200)
    # specialization = models.CharField(max_length=30)
    city = models.CharField(max_length=40,default="None")
    state = models.CharField(max_length=30)
    country = models.CharField(default="India", max_length=30)
    established = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    modified_by = models.ForeignKey(User, null=True, blank=True)
    type_of_institute = models.CharField(max_length = 5, default="None")
    misc = models.CharField(blank=True, null=True, max_length=100)
    is_normalized = models.BooleanField(default=True)


    def __unicode__(self):
        return u'%s' % self.name

        
    @property
    def no_of_matches(self):
        key = "matches::%s" % self.pk
        count = cache.get(key)
        if count:
            return count

        count = self.norm_string_set.filter(models.Q(status=1)).count()
        cache.set(key, count)

        return count

    @property
    def has_match(self):
        return bool(self.no_of_matches)

    def get_matches(self):

        #TODO: Implement logic to return matches
        #      for the given object.

        results = []
        matches = InstituteMatches.objects.filter(models.Q(normalized_inst_id=self) & models.Q(status=1))
        
        for match in matches:
            matched_object = match.get_match(self)

            # print "match id", match.id
            # print "match score" , match.match_score
            # print "match status", match.status
            # print "matched_object id", matched_object['id']
            # print "matched_object content", matched_object['content']

            x = {
                "id": match.id,
                "match_percentile": match.match_score,
                "status": match.status,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content']
                }
            }
        
            results.append(x)

        return results


class UnnormalizedInstitute(models.Model):

    name = models.CharField(max_length=200)
    status = models.IntegerField(default=0)

class InstituteAlias(models.Model):

    normalized_institute = models.ForeignKey(NormalizedInstitute, related_name='norm_set')
    ins_alias_name = models.ForeignKey(UnnormalizedInstitute, related_name='alias_set')



class InstituteMatches(models.Model):

    normalized_inst = models.ForeignKey(NormalizedInstitute,related_name='norm_string_set')
    unnormalized_inst = models.ForeignKey(UnnormalizedInstitute,related_name='unnorm_string_set')
    match_score = models.IntegerField(default=0)
    status = models.IntegerField(default=0)



    def get_match(self, against):
        
        match_info = {}
        
        if against.pk == self.normalized_inst.pk:
            match_info['id'] = self.id
            match_info['content'] = self.unnormalized_inst.name
            print "Content = ", self.unnormalized_inst.name
            return match_info
        
        return None

    @property
    def name(self):
        return self.unnormalized_inst.name

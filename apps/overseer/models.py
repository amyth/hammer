from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

class InstituteType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.name


class NormalizedInstitute(models.Model):

    name = models.CharField(max_length=200, db_index=True)
    city = models.CharField(max_length=40,default="None")
    state = models.CharField(max_length=30)
    country = models.CharField(default="India", max_length=30)
    established = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    # modified_by = models.ForeignKey(User)
    type_of_institute = models.ForeignKey(InstituteType)
    misc = models.CharField(blank=True, null=True, max_length=100)
    no_of_matches = models.IntegerField(default=0)
    no_of_approved_matches = models.IntegerField(default=0)
    no_of_aliases = models.IntegerField(default=0)
    cummulative_matches = models.IntegerField(default=0)


    def __unicode__(self):
        return u'%s' % self.name

    @property
    def has_match(self):
        return bool(self.no_of_matches)

    @property
    def has_approved_match(self):
        return bool(self.no_of_approved_matches)
    
    @property
    def has_aliases(self):
        return bool(self.no_of_aliases)    



    #  Implement logic to return matches
    #  for the given normalized institute.

    def get_matches(self):

        results = []
        matches = InstituteMatches.objects.filter(
            models.Q(normalized_inst_id=self) & models.Q(status=1)).order_by(
                '-unnormalized_inst__frequency')
        
        for match in matches:
            matched_object = match.get_match(self)   ## get_match from the InstituteMatches model

            x = {
                "id": match.id,
                "match_percentile": match.match_score,
                "status": match.status,
                "norm_string": match.normalized_inst.name,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content'],
                    "frequency": matched_object['frequency']
                }
            }
        
            results.append(x)

        return results

    #  Implement logic to return approved matches
    #  for the given normalized institute.
    

    def get_approved_matches(self):


        results = []
        appr_matches = InstituteMatches.objects.filter(
                models.Q(normalized_inst_id=self) & models.Q(status=2)).order_by(
                '-match_score')

        for match in appr_matches:
            matched_object = match.get_match(self)   ## get_match from the InstituteMatches model 

            x = {
                "id": match.id,
                "match_percentile": match.match_score,
                "status": match.status,
                "norm_string": match.normalized_inst.name,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content']
                }
            }
            
            results.append(x)

        return results


    def get_discarded_matches(self):


        results = []
        disc_matches = InstituteMatches.objects.filter(
                models.Q(normalized_inst_id=self) & (models.Q(status=3) | models.Q(status=5))).order_by(
                '-match_score')

        for match in disc_matches:
            matched_object = match.get_match(self)   ## get_match from the InstituteMatches model 

            x = {
                "id": match.id,
                "match_percentile": match.match_score,
                "status": match.status,
                "norm_string": match.normalized_inst.name,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content']
                }
            }
            
            results.append(x)

        return results   


    def get_skipped_matches(self):


        results = []
        skip_matches = InstituteMatches.objects.filter(
                models.Q(normalized_inst_id=self) & models.Q(status=4)).order_by(
                '-match_score')

        for match in skip_matches:
            matched_object = match.get_match(self)   ## get_match from the InstituteMatches model 

            x = {
                "id": match.id,
                "match_percentile": match.match_score,
                "status": match.status,
                "norm_string": match.normalized_inst.name,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content']
                }
            }
            
            results.append(x)

        return results


    def get_approved_aliases(self):


        results = []
        aliases = InstituteAlias.objects.filter(models.Q(normalized_institute_id=self))

        for alias in aliases:
            matched_object = alias.get_alias_match(self)     ## get_alias_match from the InstituteMatches model

            x = {
                "id": alias.id,
                "norm_string": alias.normalized_institute.name,
                "match": {
                    "id": matched_object['id'],
                    "content": matched_object['content']
                }
            }
        
            results.append(x)

        return results



class UnnormalizedInstitute(models.Model):

    name = models.CharField(max_length=200)
    frequency = models.IntegerField(default=1)
    no_of_matches = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def get_matches(self):

            results = []
            matches = InstituteMatches.objects.filter(
                models.Q(unnormalized_inst_id=self) & models.Q(status=1)).order_by(
                    '-match_score')
            
            for match in matches:
                matched_object = match.get_norm_match(self)

                x = {
                    "id": match.id,
                    "match_percentile": match.match_score,
                    "status": match.status,
                    "unnorm_string": match.unnormalized_inst.name,
                    "match": {
                        "id": matched_object['id'],
                        "content": matched_object['content'],
                    }
                }
            
                results.append(x)

            return results



class InstituteAlias(models.Model):

    normalized_institute = models.ForeignKey(NormalizedInstitute, related_name='norm_set')
    ins_alias= models.CharField(max_length=200)

    def get_alias_match(self, against):
        
        match_info = {}
        
        if against.pk == self.normalized_institute.pk:
            match_info['id'] = self.id
            match_info['content'] = self.ins_alias
            return match_info
        
        return None

class InstituteMatches(models.Model):

    normalized_inst = models.ForeignKey(NormalizedInstitute, related_name='norm_string_set')
    unnormalized_inst = models.ForeignKey(UnnormalizedInstitute, related_name='unnorm_string_set')
    match_score = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    '''

    status values and corresponding tag

    status value 1 = unapproved match
    status value 2 = approved match
    status value 3 = manual discarded match
    status value 4 = skipped match
    status value 5 = auto discarded match

    '''

    def get_match(self, against):
        
        match_info = {}
        
        if against.pk == self.normalized_inst.pk:
            match_info['id'] = self.id
            match_info['content'] = self.unnormalized_inst.name
            match_info['frequency'] = self.unnormalized_inst.frequency
            return match_info
        
        return None

    def get_norm_match(self, against):
        
        match_info = {}
        
        if against.pk == self.unnormalized_inst.pk:
            match_info['id'] = self.id
            match_info['content'] = self.normalized_inst.name
            return match_info
        
        return None

    @property
    def name(self):
        return self.normalized_inst.name


from django.db import models

from cbe.party.models import PartyRole
from cbe.customer.models import CustomerAccount
from cbe.credit.models import Credit

job_status_choices = (('active', 'active'), ('complete', 'complete'),)

class Job(models.Model):
    created = models.DateField(auto_now_add=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    job_number = models.CharField(max_length=200)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    
    job_status = models.CharField(max_length=100, choices=job_status_choices)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s for account %s"%(self.job_number, self.account)

        
class JobPartyRole(PartyRole):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_party_roles")
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s of %s on job %s"%(self.name, self.party, self.job.job_number)

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = "JobPartyRole"
        super(JobPartyRole, self).save(*args, **kwargs)
        
        
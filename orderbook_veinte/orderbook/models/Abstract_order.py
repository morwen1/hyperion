
#DJANGO
from django.db import models 




#MODELS
class AbOrderbook (models.Model):
    """
        modelo abstracto para todos los created_at y los deleted_at uptadeted_at
    """

    created_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False , null=True)
    uptadeted_at = models.DateTimeField(auto_now=False , null=True)
    

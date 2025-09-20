from django.db import models


# ---------------------------------------- CONTENT MODEL ----------------------------------------
class ContentModel(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title




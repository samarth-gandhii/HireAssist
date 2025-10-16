from django.db import models
from django.shortcuts import render

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def candidate_name(self):
        # derive candidate name from file name
        return self.file.name.split('/')[-1].split('.')[0]

    def __str__(self):
        return self.candidate_name()


class Employee(models.Model):
    name = models.CharField(max_length=255)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.TextField(blank=True)  # Store ranked skills
    score = models.IntegerField(default=0)  # Ranking score
    hired_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    credit_hours = models.IntegerField(choices=[(2, '2 Credit Hours'), (3, '3 Credit Hours')])

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('student', 'course')

class Assessment(models.Model):
    name = models.CharField(max_length=20)
    max_score = models.IntegerField()
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.FloatField()
    
    class Meta:
        unique_together = ('enrollment', 'assessment')

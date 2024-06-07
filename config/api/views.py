from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .permissions import *
from rest_framework import viewsets, permissions
from .models import Course, Enrollment, Grade
from .serializers import CourseSerializer, EnrollmentSerializer, GradeSerializer
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Create your views here.

@api_view(['GET'])
def index(request):
    return Response({'message': 'Hello World'}, status=status.HTTP_200_OK) # Making sure everything is working fine


class UploadGradesView(APIView):
    parser_classes = [FileUploadParser]
    
    def post(self, request, format=None):
        file_obj = request.FILES['file']
        df = pd.read_excel(file_obj)
        
        for index, row in df.iterrows():
            student_id = row['studentid']
            try:
                student = User.objects.get(username=student_id)
            except ObjectDoesNotExist:
                continue

            for col in ['a1', 'a2', 'a3', 'q1', 'q2', 'q3', 'mids', 'finals']:
                score = row[col]
                assessment = Assessment.objects.get(name=col.upper())
                enrollment = Enrollment.objects.get(student=student, course=assessment.course)
                Grade.objects.update_or_create(
                    enrollment=enrollment,
                    assessment=assessment,
                    defaults={'score': score}
                )
                
        return Response({'status': 'grades uploaded successfully'})



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Students').exists():
            return Grade.objects.filter(enrollment__student=user)
        return Grade.objects.all()

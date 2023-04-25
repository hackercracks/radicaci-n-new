from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView,
    ListCreateAPIView
)
from .serializers import ( 
    FileSerializer, FileCreateSerializer, AssignAgentSerializer, 
    AssignFileAgentSerializer, VeriyDocSerializer, 
    ObservationSerializer, ReviewSerializer, DocumentSerializer,
    ActProcedureSerializer, PaymentDocSerializer, PaymentSerializer,
    ResolutionSerializer, ResolutionNotificationSerializer, UnderReviewSerializer,
    NotifiedSerializer, PersonalNotifiedSerializer, FileTypeSerializer, AllTrackSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from filed.models import File, Agent, Category, VeriyDoc, FileType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.filters import SearchFilter


class FileNumView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # query last value of file unique number
        get_file = File.objects.all()
        if get_file.exists():
            print("Has Data")
            # last_file = File.objects.filter(organisation=2).order_by('-id')[0]
            last_file = File.objects.all().order_by('-id')[0]
            file_num = int(last_file.file_name) + 1
            d = "%05d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%05d" % ( file_num, )
            print(d)

        return Response(d)

class FileSearchView(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=file_name']
    
class FileListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # files = File.objects.all()
        unassigned_files = File.objects.filter(agent__isnull=True)

        user = self.request.user
        # queryset = File.objects.filter(agent__isnull=False)
        if user.is_organisor:
            queryset = File.objects.filter(agent__isnull=False)
        else:
            queryset = File.objects.filter(agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        serializerFile = FileSerializer(queryset, many=True)
        unassignedFile = FileSerializer(unassigned_files, many=True)


        # query last value of file unique number
        # get_file = File.objects.filter(organisation=2)
        get_file = File.objects.all()
        if get_file.exists():
            print("Has Data")
            # last_file = File.objects.filter(organisation=2).order_by('-id')[0]
            last_file = File.objects.all().order_by('-id')[0]
            file_num = int(last_file.file_name) + 1
            d = "%05d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%05d" % ( file_num, )
            print(d)

        if user.is_organisor or user.is_support:
            x_id = user.userprofile.id
        else:
            x_id = ""
        
        print("x_id", x_id)

        return Response({
            "user_id": user.id,
            "user_profile": x_id,
            "fileNum": d,
            "files": serializerFile.data,
            "unassigned_files": unassignedFile.data
        })

    def post(self, request, format=None):
        serializer = FileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data["file_type"])

            # ====== send email notification ===== #
            # email = serializer.data["email"]
            # subject= 'A File has been created'
            # message= f"Go to the site to see the new File"
            # from_email= settings.EMAIL_HOST_USER
            # recipient_list=[email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class FileDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        print(filed.id)

        verifyy = VeriyDoc.objects.filter(filev = filed.id)
        # verifySerializer = VeriyDocSerializer(verifyy)
        if verifyy.exists():
            print("Has data")
            verifyy = VeriyDoc.objects.get(filev = filed.id)
            verifySerializer1 = VeriyDocSerializer(verifyy)
            verifySerializer = verifySerializer1.data
        else:
            print("No Data")
            verifySerializer = None

        serializer = FileSerializer(filed)
        return Response({
            "status": "success",
            "files" : serializer.data,
            "verify" : verifySerializer
            })

    def put(self, request, pk, format=None):
        filed = self.get_object(pk)
        serializer = FileCreateSerializer(filed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        filed = self.get_object(pk)
        filed.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class FileDetailViewII(RetrieveAPIView):
    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        filed = self.get_object(pk)
        print(filed.id)

        serializer = FileSerializer(filed)
        return Response(serializer.data)


class TrackDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AllTrackSerializer
    queryset = File.objects.all()

class verifyDocCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = VeriyDocSerializer
    queryset = VeriyDoc.objects.all()

class verifyDocUpdateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = VeriyDocSerializer
    queryset = VeriyDoc.objects.all()

class verifyDocDeleteView(DestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = VeriyDoc.objects.all()

class AssignAgentView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = AssignFileAgentSerializer
    queryset = File.objects.all()

class AssignAgentRetrieveView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        user = self.request.user
        queryset = Agent.objects.all()
        allAgent = AssignAgentSerializer(queryset, many=True)

        return Response( allAgent.data)

class FileTypeView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FileTypeSerializer
    queryset = FileType.objects.all()

class UnderReview(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UnderReviewSerializer
    queryset = File.objects.all()

class ReviewView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ReviewSerializer
    queryset = File.objects.all()

class ObservationView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ObservationSerializer
    queryset = File.objects.all()

class NotifiedView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = NotifiedSerializer
    queryset = File.objects.all()

class DocumentView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DocumentSerializer
    queryset = File.objects.all()

class ActProcedureView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ActProcedureSerializer
    queryset = File.objects.all()

class PersonalNotifiedView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PersonalNotifiedSerializer
    queryset = File.objects.all()

class PaymentView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentSerializer
    queryset = File.objects.all()

class PaymentDocView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentDocSerializer
    queryset = File.objects.all()

class ResolutionView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResolutionSerializer
    queryset = File.objects.all()

class ResolutionNotificationView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResolutionNotificationSerializer
    queryset = File.objects.all()



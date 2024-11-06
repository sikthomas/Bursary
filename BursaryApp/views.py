from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,PersonalInformationForm,InstitutionInformationForm,BothParentForm,FatherForm,MotherForm,GuardianForm,ParentTypeChoiceForm,AdditionalInformationForm,VerificationForm,AllocationForm,UsertypeForm
from .models import PersonalInformation,InstitutionalInformation,BotheParent,Mother,Father,Guardian,AdditionalInformation,CustomUser,ParentType,Verification,Allocation,Usertype

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not hasattr(user, 'backend'):
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'User added successfully')
            return redirect('login_view')
        else:
            # If the form is not valid, render the form with errors
            return render(request, 'superuser/signup.html', {'form': form})
    else:
        # For GET requests, display the empty form
        form = SignupForm()
        return render(request, 'superuser/signup.html', {'form': form})
 
def login_view(request):
    if request.method == 'POST':
        idnumber = request.POST.get('idnumber')
        password = request.POST.get('password')
        
        # Authenticate using idnumber instead of username
        user = authenticate(request, idnumber=idnumber, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser and user.is_staff and user.is_finance:
                messages.success(request, 'Logged in Successfully')
                return redirect('adminindex2') 
            elif not user.is_superuser and not user.is_staff and not user.is_finance:
                messages.success(request, 'Logged in Successfully')
                return redirect('index') 
            else:
                messages.success(request, 'Logged in Successfully')
                return redirect('adminindex') 
        else:
            messages.info(request, 'Account does not exist or incorrect credentials, please try again')

    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Log in'})

@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        return redirect('login_view')  
    
    return render(request, 'accounts/logout.html')


def index(request):
    user = request.user

    fullapplication = CustomUser.objects.filter(id=user.id, personal_information=True,institution_information=True,parent_information=True,additional_information=True).exists()
    
    personal_information = CustomUser.objects.filter(id=user.id, personal_information=True).exists()
    institution_information = CustomUser.objects.filter(id=user.id, institution_information=True).exists()
    parent_type = CustomUser.objects.filter(id=user.id, parent_type=True).exists()
    additional_information = CustomUser.objects.filter(id=user.id, additional_information=True).exists()
    parent_information = CustomUser.objects.filter(id=user.id, parent_information=True).exists()

    # Check application status
    application_status = (personal_information and institution_information and 
                          parent_information and additional_information)

    # Check verification statuses
    verification = Verification.objects.filter(verified_by=user).exists()
    approved_status = Verification.objects.filter(verified_by=user, status='accepted').exists()
    declined_status = Verification.objects.filter(verified_by=user, status='declined').exists()

    # Get allocation details
    allocation = Allocation.objects.filter(verified_id__applicant_id__userid=user).first()
    allocated_amount = allocation.allocated_amount if allocation else None

    return render(request, "student/index.html", {
        'parent_type': parent_type,
        'application_status': application_status,
        'approved_status': approved_status,
        'declined_status': declined_status,
        'allocated_amount': allocated_amount,
        'personal_information': personal_information,
        'institution_information': institution_information,
        'parent_information': parent_information,
        'additional_information': additional_information,
        'verification': verification,
        'fullapplication':fullapplication
    })


def adminindex(request):
    users = CustomUser.objects.count()
    applications = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=True, additional_information=True).count()
    updo_personalinformation = CustomUser.objects.filter(personal_information=True, institution_information=False, parent_information=False, additional_information=False).count()
    upto_institution = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=False, additional_information=False).count()
    upto_parent = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=True, additional_information=False).count()
    approved_students = Verification.objects.filter(status='accepted').count()
    declined_students = Verification.objects.filter(status='declined').count()
    allocated = Allocation.objects.all().count() 

    return render(request, 'admindashboard/index.html', {
            'users': users,
            'applications': applications,
            'updo_personalinformation': updo_personalinformation,
            'upto_institution': upto_institution,
            'upto_parent': upto_parent,
            'approved_students': approved_students,
            'declined_students': declined_students,
            'allocated': allocated,
            
        })


def adminindex2(request):
    users = CustomUser.objects.count()
    applications = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=True, additional_information=True).count()
    updo_personalinformation = CustomUser.objects.filter(personal_information=True, institution_information=False, parent_information=False, additional_information=False).count()
    upto_institution = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=False, additional_information=False).count()
    upto_parent = CustomUser.objects.filter(personal_information=True, institution_information=True, parent_information=True, additional_information=False).count()
    approved_students = Verification.objects.filter(status='accepted').count()
    declined_students = Verification.objects.filter(status='declined').count()
    allocated = Allocation.objects.all().count()  

    return render(request, 'superuser/index2.html', {
            'users': users,
            'applications': applications,
            'updo_personalinformation': updo_personalinformation,
            'upto_institution': upto_institution,
            'upto_parent': upto_parent,
            'approved_students': approved_students,
            'declined_students': declined_students,
            'allocated': allocated,
            
        })


@login_required
def personalInformation(request):
    user = request.user
    personal_info = CustomUser.objects.filter(id=user.id, personal_information=True).exists()
    personal_information = CustomUser.objects.filter(username=user.username).first()
    update_personalinformation=CustomUser.objects.get(username=user.username)
    
    try:
        personal_info = PersonalInformation.objects.get(userid=user)
    except PersonalInformation.DoesNotExist:
        personal_info = None

    if request.method == 'POST':
        form = PersonalInformationForm(request.POST, request.FILES,instance=personal_info)
        if form.is_valid():
            update_personalinformation.personal_information=True
            update_personalinformation.save()

            personal_info = form.save(commit=False)
            personal_info.userid = user
            personal_info.save()
            messages.success(request, 'Personal information saved successifully')
            return redirect('index')  # Redirect to a relevant page after saving
    else:
        form = PersonalInformationForm(instance=personal_info)

    return render(request, 'student/personalinformation.html', {'form': form,'personal_information':personal_information,'personal_info':personal_info})

def parent_type(request):
    user = request.user
    update_parent_type=CustomUser.objects.get(username=user.username)
    

    # Get or create the ParentType instance for the current user
    parent_type,created = ParentType.objects.get_or_create(user_id=user)

    if request.method == 'POST':
        form = ParentTypeChoiceForm(request.POST)
        if form.is_valid():
            update_parent_type.parent_type=True
            update_parent_type.save()   

            choice = form.cleaned_data['parent_type']
            
            # Update ParentType fields based on the selected choice
            if choice == 'both_parents':
                parent_type.bother_parent = True
                parent_type.father = False
                parent_type.mother = False
                parent_type.mother = False
                parent_type.user_id=user
            elif choice == 'mother':
                parent_type.bother_parent = False
                parent_type.father = False
                parent_type.mother = False
                parent_type.mother = True
                parent_type.user_id=user
            elif choice == 'father':
                parent_type.bother_parent = False
                parent_type.father = True
                parent_type.mother = False
                parent_type.guardian = False
                parent_type.user_id=user
            elif choice == 'guardian':
                parent_type.bother_parent = False
                parent_type.father = False
                parent_type.mother = False
                parent_type.guardian = True
                parent_type.user_id=user
            parent_type.save()
            messages.success(request, 'Parent saved successifully')
            return redirect('familyInformation')  # Redirect after successful save
    else:
        form = ParentTypeChoiceForm()

    return render(request, 'student/parent_type.html', {'form': form})

def institutionInformation(request):
    user = request.user
    institution = CustomUser.objects.filter(id=user.id, institution_information=True).exists()
    institution_information = CustomUser.objects.filter(username=user.username).first()
    update_institution=CustomUser.objects.get(username=user.username)
    try:
        student_info = PersonalInformation.objects.get(userid=user)
    except PersonalInformation.DoesNotExist:
        student_info = None

    try:
        institution_info = InstitutionalInformation.objects.get(application=student_info)
    except InstitutionalInformation.DoesNotExist:
        institution_info = None

    if request.method == 'POST':
        form = InstitutionInformationForm(request.POST,request.FILES, instance=institution_info)
        if form.is_valid():
            update_institution.institution_information=True
            update_institution.save()

            institution_info = form.save(commit=False)
            institution_info.application = student_info
            institution_info.save()
            messages.success(request, 'Institution saved successifully')
            return redirect('index')  # Redirect to a relevant page after saving
    else:
        form = InstitutionInformationForm(instance=institution_info)

    return render(request, 'student/institutioninformation.html', {'form': form,'institution_information':institution_information,'institution':institution})

def familyInformation(request):
    user = request.user
    parent_information = CustomUser.objects.filter(username=user.username).first()
    update_familyInformation=CustomUser.objects.get(username=user.username)
    form_type = request.GET.get('form_type')  # Get the form type from the query parameters
    instance = None  # Initialize instance to handle cases where it might not be defined

    # Fetch personal information for the current user
    try:
        personal_info = PersonalInformation.objects.get(userid=user)
    except PersonalInformation.DoesNotExist:
        personal_info = None

    # Determine which form to use based on ParentType fields
    try:
        parent_type = ParentType.objects.get(user_id=user)
    except ParentType.DoesNotExist:
        parent_type = None

    if parent_type:
        if parent_type.bother_parent:
            instance, created = BotheParent.objects.get_or_create(applicant_id=personal_info)
            form = BothParentForm(instance=instance)
        elif parent_type.mother:
            instance, created = Mother.objects.get_or_create(applicant_id=personal_info)
            form = MotherForm(instance=instance)
        elif parent_type.father:
            instance, created = Father.objects.get_or_create(applicant_id=personal_info)
            form = FatherForm(instance=instance)
        elif parent_type.guardian:
            instance, created = Guardian.objects.get_or_create(applicant_id=personal_info)
            form = GuardianForm(instance=instance)
        else:
            # Handle the case where no parent type is set
            form = None

    if request.method == 'POST' and form:
        form = form.__class__(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            update_familyInformation.parent_information=True
            update_familyInformation.save()
            
            form.save()
            messages.success(request, 'Parent saved successifully')
            return redirect('index')  # Redirect after saving

    return render(request, 'student/familyinformation.html', {'form': form,'parent_information':parent_information})

def additionalInformation(request):
    user = request.user
    additional_information = CustomUser.objects.filter(username=user.username).first()
    update_additionalInformation = CustomUser.objects.get(username=user.username)

    # Get the PersonalInformation instance related to the logged-in user
    try:
        personal_info = PersonalInformation.objects.get(userid=user)
    except PersonalInformation.DoesNotExist:
        personal_info = None  # Handle this case as needed

    if not personal_info:
      
        return redirect('index')  

    additional_info, created = AdditionalInformation.objects.get_or_create(studentsid=personal_info)

    if request.method == 'POST':
        form = AdditionalInformationForm(request.POST, instance=additional_info)
        if form.is_valid():
            update_additionalInformation.additional_information = True
            update_additionalInformation.save()

            additional_info = form.save(commit=False)
            additional_info.studentsid = personal_info  # Ensure the correct PersonalInformation is set
            additional_info.save()

            messages.success(request, 'Assesment information saved successifully')
            return redirect('index')  # Replace with your success page URL or name
    else:
        form = AdditionalInformationForm(instance=additional_info)
    return render(request, 'student/additionalinformation.html', {'form': form, 'additional_information': additional_information})

def applicant_list(request):
    verified_student = Verification.objects.filter(status='accepted')
    declined_student = Verification.objects.filter(status='declined')
    users = CustomUser.objects.all()
    applications = PersonalInformation.objects.count()
    
    # Filter PersonalInformation based on the related CustomUser fields
    personalInformation = PersonalInformation.objects.filter(
        userid__personal_information=True,
        userid__institution_information=True,
        userid__parent_information=True,
        userid__additional_information=True
    )

    institutionInformation = InstitutionalInformation.objects.all()
    bothparentInformation = BotheParent.objects.all()
    fatherInformation = Father.objects.all()
    motherInformation = Mother.objects.all()
    guardianInformation = Guardian.objects.all()

    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()

    if currentuser:
        return render(request, 'superuser/applicantlist.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
            'bothparentInformation': bothparentInformation,
            'fatherInformation': fatherInformation,
            'motherInformation': motherInformation,
            'guardianInformation': guardianInformation,
            'applications': applications,
            'users': users,
            'verified_student':verified_student,
            'declined_student':declined_student
        })
    else:
        return render(request, 'admindashboard/applicantlist.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
            'bothparentInformation': bothparentInformation,
            'fatherInformation': fatherInformation,
            'motherInformation': motherInformation,
            'guardianInformation': guardianInformation,
            'applications': applications,
            'users': users,
            'verified_student':verified_student,
            'declined_student':declined_student
        })

def pending_personalInformation(request):
    personalInformation = PersonalInformation.objects.filter(
        userid__personal_information=True,
        userid__institution_information=False,
        userid__parent_information=False,
        userid__additional_information=False
    )

    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()

    if currentuser:
        return render(request, 'superuser/pending_personalinfo.html', {
            'personalInformation': personalInformation 
        })
    else:
        return render(request, 'admindashboard/pending_personalinfo.html', {
            'personalInformation': personalInformation 
        })

def pending_institutionInformation(request):
    personalInformation = PersonalInformation.objects.filter(
        userid__personal_information=True,
        userid__institution_information=True,
        userid__parent_information=False,
        userid__additional_information=False
    )

    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()
    institutionInformation = InstitutionalInformation.objects.all()

    if currentuser:
        return render(request, 'superuser/pending_institution.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
        })
    else:
        return render(request, 'admindashboard/pending_institution.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
        })

def pending_parentInformation(request):
    # Filter PersonalInformation based on the related CustomUser fields
    personalInformation = PersonalInformation.objects.filter(
        userid__personal_information=True,
        userid__institution_information=True,
        userid__parent_information=True,
        userid__additional_information=False
    )
    institutionInformation = InstitutionalInformation.objects.all()

     
    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()

    if currentuser:
        return render(request, 'superuser/pending_parents.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
        })
    else:
         return render(request, 'admindashboard/pending_parents.html', {
            'personalInformation': personalInformation,
            'institutionInformation': institutionInformation,
        })
    
def applicant_details(request, pk):
    personal_information = get_object_or_404(PersonalInformation, pk=pk)
    institution_information = InstitutionalInformation.objects.filter(application=personal_information)
    additional_information=AdditionalInformation.objects.filter(studentsid=personal_information)
    parent_type = get_object_or_404(ParentType, user_id=personal_information.userid)

    bothparent = BotheParent.objects.filter(applicant_id=personal_information) if parent_type.bother_parent else None
    father = Father.objects.filter(applicant_id=personal_information) if parent_type.father else None
    mother = Mother.objects.filter(applicant_id=personal_information) if parent_type.mother else None
    guardian = Guardian.objects.filter(applicant_id=personal_information) if parent_type.guardian else None

    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()

    if currentuser:
        return render(request, 'superuser/applicantdetails.html', {
            'student': personal_information,
            'institutionInformation': institution_information,
            'parent_type': parent_type,
            'bothparent': bothparent,
            'father': father,
            'mother': mother,
            'guardian': guardian,
            'additional_information':additional_information
        })
    else:
        return render(request, 'admindashboard/applicantdetails.html', {
            'student': personal_information,
            'institutionInformation': institution_information,
            'parent_type': parent_type,
            'bothparent': bothparent,
            'father': father,
            'mother': mother,
            'guardian': guardian,
            'additional_information':additional_information
        })

def verify_applicantion(request, pk):
    user = request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()
    update_verification=CustomUser.objects.get(username=user.username)
    applicant = get_object_or_404(PersonalInformation, pk=pk)
    
    try:
        verification = Verification.objects.get(applicant_id=applicant)
    except Verification.DoesNotExist:
        
        verification = Verification.objects.create(applicant_id=applicant, verified_by=request.user)

    if request.method == 'POST':
        form = VerificationForm(request.POST, instance=verification)
        if form.is_valid():
            update_verification.verification_stutus=True
            update_verification.save()

            verification = form.save(commit=False)
            verification.verified_by = request.user 
            verification.save()
            messages.success(request, 'Verification successiful')
            return redirect('adminindex2') 
    else:
        form = VerificationForm(instance=verification)

        if currentuser:
            return render(request, 'superuser/verification.html', {'form': form, 'applicant': applicant})
        else:
            return render(request, 'admindashboard/verification.html', {'form': form, 'applicant': applicant})

def verified_applications(request):
    user = request.user
    currentuser = CustomUser.objects.filter(id=user.id, is_superuser=True, is_staff=True, is_finance=True).exists()
    
    verified_students = Verification.objects.filter(status='accepted')
    allocations = Allocation.objects.all()
    allocation_dict = {allocation.verified_id.id: allocation for allocation in allocations}

    template_name = 'superuser/verified.html' if currentuser else 'admindashboard/verified.html'

    return render(request, template_name, {
        'verified_students': verified_students,
        'allocation_dict': allocation_dict,
    })

def declined_applications(request):
    user=request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()
    declined_student = Verification.objects.filter(status='declined')

    if currentuser:
        return render(request, 'superuser/declined.html', {'declined_student': declined_student})
    else:
         return render(request, 'admindashboard/declined.html', {'declined_student': declined_student})


def allocation(request, pk):
    user = request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()
    update_allocation = CustomUser.objects.get(username=user.username)
    verified_applicant = get_object_or_404(Verification, pk=pk)
    
    try:
        allocation = Allocation.objects.get(verified_id=verified_applicant)
    except Allocation.DoesNotExist:
        allocation = Allocation.objects.create(verified_id=verified_applicant, allocated_by=request.user, allocated_amount=0)  # Provide a default value

    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            update_allocation.allocation_stutus = True
            update_allocation.save()

            allocation = form.save(commit=False)
            allocation.allocated_by = request.user 
            allocation.save()
            messages.success(request, 'Allocation successiful')
            return redirect('adminindex') 
    else:
        form = AllocationForm(instance=allocation)

        if currentuser:
            return render(request, 'superuser/allocation.html', {'form': form, 'verified_applicant': verified_applicant})
        else:
            return render(request, 'admindashboard/allocation.html', {'form': form, 'verified_applicant': verified_applicant})

def allocated_list(request):
    user = request.user
    currentuser= CustomUser.objects.filter(id=user.id, is_superuser=True,is_staff=True,is_finance=True).exists()
    allocated = Allocation.objects.all()

    if currentuser:
        return render(request, 'superuser/allocatedlist.html', {'allocated': allocated})
    else:
        return render(request, 'admindashboard/allocatedlist.html', {'allocated': allocated})

def role(request):
    if request.method == 'POST':
        form = UsertypeForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('userid')
            role = form.cleaned_data.get('role')
            
            # Reset user roles
            user.is_superuser = False
            user.is_staff = False
            user.is_finance = False

            if role == 'superuser':
                user.is_superuser = True
                user.is_staff = True
                user.is_finance = True
            elif role == 'fundmanager':
                user.is_staff = True
                user.is_finance = True
            elif role == 'staff':
                user.is_staff = True
            elif role == 'student':
                user.is_superuser = False
                user.is_staff = False
                user.is_finance = False

            user.save()
            
            # Create or update Usertype instance
            Usertype.objects.update_or_create(
                userid=user, defaults={'role': role}
            )

            messages.success(request, 'Role updated successfully')
            return redirect('adminindex2')  # Ensure 'adminindex' is a valid URL name
        else:
            messages.error(request, 'Invalid form submission')
    
    else:
        form = UsertypeForm()
    
    return render(request, 'superuser/assignrole.html', {'form': form})

def systemUsers(request):
    users=CustomUser.objects.all()
    return render(request,'superuser/users.html',{'users':users})

def deleteUser(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('adminindex2')
    return render(request, 'superuser/delete.html', {'user': user})


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PersonalInformation, InstitutionalInformation, BotheParent, Father, Mother, Guardian, ParentType, AdditionalInformation, Verification, Allocation, Usertype

class SignupForm(UserCreationForm):
    CONSTITUENCY_CHOICES = [
        ('', 'Select your constituency'),
        ('Navakholo', 'Navakholo'),
        ('Embakasi East', 'Embakasi East'),
    ]
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Last Name'
        })
    )
    idnumber = forms.IntegerField(
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'ID/Birth Certificate'
        })
    )
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Email Address'
        })
    )
    constituency = forms.ChoiceField(
        choices=CONSTITUENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'idnumber', 'constituency', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Last Name'
        })
        self.fields['idnumber'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'ID/Birth Certificate'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Email Address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-user',
            'placeholder': 'Repeat Password'
        })


class PersonalInformationForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('', 'Select your gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    WARD_CHOICES = [
         ('', 'Select your ward'),
        ('Bunyala east', 'Bunyala East'),
        ('Bunyala central', 'Bunyala Central'),
        ('Bunyala west', 'Bunyala West'),
        ('Shinoyi shikomary', 'Shinoyi Shikomari'),
    ]

    VILLAGE_CHOICES = [
        ('', 'Select your village'),
        ('Muregu', 'Muregu'),
        ('Musaga', 'Musaga'),
        ('Makhima', 'Makhima'),
        ('Lutaso', 'Lutaso'),
        ('Namirama', 'Namirama'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    ward = forms.ChoiceField(choices=WARD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    village = forms.ChoiceField(choices=VILLAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = PersonalInformation
        fields = ['gender', 'date_of_birth', 'phone_number', 'ward', 'village','applicand_id']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}),
            'applicand_id': forms.FileInput(attrs={'class': 'form-control'}),
        }

class InstitutionInformationForm(forms.ModelForm):
    INSTITUTION_CATEGORY = [
        ('', 'Select Institution Category'),
        ('University', 'University'),
        ('TVET', 'TVET'),
        ('KMTC', 'KMTC'),
        ('County Polytechnic', 'County Polytechnic'),
    ]

    MODE_OF_STUDY = [
        ('', 'Select Mode of Study'),
        ('Regular', 'Regular'),
        ('Pallel', 'Parallel'),
        ('Boarding', 'Boarding'),
        ('Day', 'Day'),
    ]
    
    COURSE_DURATION = [
         ('', 'Select course duration'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]

    institution_category = forms.ChoiceField(choices=INSTITUTION_CATEGORY, widget=forms.Select(attrs={'class': 'form-control'}))
    mode_of_study = forms.ChoiceField(choices=MODE_OF_STUDY, widget=forms.Select(attrs={'class': 'form-control'}))
    course_duration = forms.ChoiceField(choices=COURSE_DURATION, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = InstitutionalInformation
        fields = [
            'institution_category',
            'institution_name',
            'admission_no',
            'course',
            'mode_of_study',
            'year_of_study',
            'course_duration',
            'year_of_completion',
            'admission_letter',
            'fee_statement'
            
            
        ]
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_study': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_of_completion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admission_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'fee_statement': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BothParentForm(forms.ModelForm):
    class Meta:
        model = BotheParent
        fields = [
            'father_firstname',
            'father_lastname',
            'father_id_no',
            'father_phone_number',
            'father_occupation',
            'father_employer',
            'father_annual_income',
            'father_id',
            'mother_firstname',
            'mother_lastname',
            'mother_id_no',
            'mother_phone_number',
            'mother_occupation',
            'mother_employer',
            'mother_annual_income',
            'mother_id'
        ]
        widgets = {
            'father_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'father_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'father_id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'father_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'father_id': forms.FileInput(attrs={'class': 'form-control'}),
            'mother_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'mother_id': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'father_firstname': ' Father First Name',
            'father_lastname': 'Father Last Name',
            'father_id_no': 'ID Number',
            'father_phone_number': 'Father Phone Number',
            'father_occupation': 'Father Occupation',
            'father_employer': 'Father Employer',
            'father_annual_income': 'Father Annual Income',
            'father_id': 'Upload ID',
            'mother_firstname': 'Mother First Name',
            'mother_firstname_lastname': 'Mother Last Name',
            'mother_id_no': 'Mother ID Number',
            'mother_phone_number': 'Mother Phone Number',
            'mother_occupation': 'Mother Occupation',
            'mother_employer': 'Mother Employer',
            'mother_annual_income': 'Mother Annual Income',
            'mother_id': 'Upload ID',

        }


# Form
class MotherForm(forms.ModelForm):
    class Meta:
        model = Mother
        fields = [
            'mother_firstname',
            'mother_lastname',  # Correct field name
            'mother_id_no',
            'mother_phone_number',
            'mother_occupation',
            'mother_employer',
            'mother_annual_income',
            'mother_id'
            
        ]
        widgets = {
            'mother_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_lastname': forms.TextInput(attrs={'class': 'form-control'}),  # Correct widget
            'mother_id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'mother_id': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'mother_firstname': 'First Name',
            'mother_lastname': 'Last Name',  # Correct label
            'mother_id_no': 'ID Number',
            'mother_phone_number': 'Phone Number',
            'mother_occupation': 'Occupation',
            'mother_employer': 'Employer',
            'mother_annual_income': 'Annual Income',
            'mother_id': 'Upload ID',
        }


class FatherForm(forms.ModelForm):
    class Meta:
        model = Father
        fields = ['father_firstname','father_lastname','father_id_no','father_phone_number','father_occupation','father_employer','father_annual_income','father_id' ]
        widgets = {
            'father_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'father_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'father_id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'father_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'father_id': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'father_firstname': 'First Name',
            'father_lastname': 'Last Name',
            'father_id_no': 'ID Number',
            'father_phone_number': 'Phone Number',
            'father_occupation': 'Occupation',
            'father_employer': 'Employer',
            'father_annual_income': 'Annual Income',
            'father_id': 'Upload ID',
        }

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['guardian_firstname','guardian_lastname','guardian_id_no','guardian_phone_number','guardian_occupation','guardian_employer','guardian_annual_income','guardian_id','father_death_certificate','mother_death_certificate']
        widgets = {
            'guardian_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'guardian_id': forms.FileInput(attrs={'class': 'form-control'}),
            'father_death_certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'mother_death_certificate': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'guardian_firstname': 'First Name',
            'guardian_firstname_lastname': 'Last Name',
            'guardian_id_no': 'ID Number',
            'guardian_phone_number': 'Phone Number',
            'guardian_occupation': 'Occupation',
            'guardian_employer': 'Employer',
            'guardian_annual_income': 'Annual Income',
            'guardian_id': 'Upload Guardian ID',
            'father_death_certificate': 'Father Death Certificate if Diseased ',
            'mother_death_certificate': 'Mother Death Certificate if Diseased',
        }
        

class ParentTypeChoiceForm(forms.ModelForm):
    CHOICES = [
        ('both_parents', 'Both Parents'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('guardian', 'Guardian'),
    ]
    
    parent_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = ParentType
        fields = []  

        

class AdditionalInformationForm(forms.ModelForm):
    AVERAGE_ACADEMIC_PERFORMANCE = [
         ('', 'Select your average academic performance'),
        ('Excellent', 'Excellent'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
    ]
    average_academic_performance = forms.ChoiceField(choices=AVERAGE_ACADEMIC_PERFORMANCE, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = AdditionalInformation
        fields = [
            'number_of_siblings',
            'main_income_source',
            'reason_for_applying',
            'average_academic_performance',
            'disability',
            'disability_name',
        ]
        widgets = {
            'number_of_siblings': forms.TextInput(attrs={'class': 'form-control'}),
            'main_income_source': forms.TextInput(attrs={'class': 'form-control'}),
            'reason_for_applying': forms.TextInput(attrs={'class': 'form-control'}),
            'disability': forms.TextInput(attrs={'class': 'form-control'}),
            'disability_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'number_of_siblings': 'Number of Siblings',
            'main_income_source': 'Main Income SourceFor Your Fee',
            'reason_for_applying': 'Reason for Applying',
            'average_academic_performance': 'Average Academic Performance',
            'disability': 'Disability',
            'disability_name': 'Disability Name',
        }

class VerificationForm(forms.ModelForm):
    VERIFICATION_CHOICES = [
         ('', 'Select Accept or Decline'),
        ('accepted', 'Accept'),
        ('declined', 'Decline'),
    ]
    status = forms.ChoiceField(choices=VERIFICATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Verification
        fields = [
            'status',
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 40})
        }
        labels = {
            'status': 'Accept /Decline the application',
            'comment': 'Reason for accepting/Declining ',
        }

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = [
            'allocated_amount',
            'comment',
        ]
        widgets = {
            'allocated_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 20})
        }
        labels = {
            'allocated_amount': 'Allocate',
            'comment': 'Reason for the amount ',
        }

class UsertypeForm(forms.ModelForm):
    ROLE_CHOICES = [
         ('', 'Select Role'),
        ('superuser', 'Superuser'),
        ('fundmanager', 'Fund Manager'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    userid = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select User"
    )

    class Meta:
        model = Usertype
        fields = ['userid', 'role']
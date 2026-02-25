from django import forms

from .models import College, Organization, OrgMember, Program, Student


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-control"
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                css = "form-check-input"
            field.widget.attrs["class"] = css


class OrganizationForm(BaseModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


class CollegeForm(BaseModelForm):
    class Meta:
        model = College
        fields = "__all__"


class ProgramForm(BaseModelForm):
    class Meta:
        model = Program
        fields = "__all__"


class StudentForm(BaseModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class OrgMemberForm(BaseModelForm):
    class Meta:
        model = OrgMember
        fields = "__all__"

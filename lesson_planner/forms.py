from cProfile import label
from django import forms
from .models import LessonPlan, Subject, LessonType, LessonStepTemplate, Grade


class LessonPlanModelForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        exclude = ["creator"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-control form-select"}),
            "subject_type": forms.Select(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "topic": forms.TextInput(attrs={"class": "form-control"}),
            "goal": forms.Textarea(attrs={"class": "form-control"}),
            "plan_file": forms.FileInput(attrs={"class": "form-control",
                                                "accept": ".docx"}),
            "equipment": forms.SelectMultiple(attrs={"class": "form-control"})
        }

    def clean_plan_file(self):
        file = self.cleaned_data.get("plan_file")
        if file:
            if not file.name.endswith(".docx"):
                raise forms.ValidationError("Разрешены только файлы DOCX")
        return file


class LessonPlanFileUploadForm(LessonPlanModelForm):
    class Meta():
        model = LessonPlan
        fields = ["plan_file"]


class SubjectModelForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "field_rename",
                                           "aria-labelledby": "help_for_field"})
        }


class SubjectTypeModelForm(forms.ModelForm):
    class Meta:
        model = LessonType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "field_add",
                                           "aria-labelledby": "help_for_field"})
        }


class LessonStepTemplateModelForm(forms.ModelForm):
    class Meta:
        model = LessonStepTemplate
        fields = ["name", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "field_add_step",
                                           "aria-labelledby": "help_for_field"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "id": "field_add",
                                              "aria-labelledby": "help_for_field"})
        }


class EditLessonStepTemplateModelForm(forms.ModelForm):
    class Meta:
        model = LessonStepTemplate
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "field_add_step",
                                           "aria-labelledby": "help_for_field"})
        }


class LessonPlanFilterForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),
                                              required=False,
                                              label="Предмет",
                                              widget=forms.CheckboxSelectMultiple)
    grades = forms.ModelMultipleChoiceField(queryset=Grade.objects.all(),
                                            required=False,
                                            label="Класс",
                                            widget=forms.CheckboxSelectMultiple)
    types_lessons = forms.ModelMultipleChoiceField(queryset=LessonType.objects.all(),
                                                   required=False,
                                                   label="Тип урока",
                                                   widget=forms.CheckboxSelectMultiple)
    date_from = forms.DateField( required=False,
                                 label="Создан после",
                                 widget=forms.DateInput(attrs={"type": "date", "class": "form-control d-inline w-75"})
    )
    date_before = forms.DateField(required=False,
                              label="Создан до",
                              widget=forms.DateInput(attrs={"type": "date", "class": "form-control d-inline w-75"})
    )

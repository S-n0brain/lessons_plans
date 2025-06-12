from django import forms
from .models import LessonPlan

class LessonPlanFileUploadForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ["plan_file"]

    def clean_plan_file(self):
        file = self.cleaned_data.get("plan_file")
        if file:
            if not file.name.endswith(".docx"):
                raise forms.ValidationError("Разрешены только файлы DOCX")
        return file


class LessonPlanModelForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = "__all__"
        widgets = {
            "subject": forms.Select(attrs={"class": "form-control"}),
            "subject_type": forms.Select(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "topic": forms.TextInput(attrs={"class": "form-control"}),
            "goal": forms.Textarea(attrs={"class": "form-control"}),
            "plan_file": forms.FileInput(attrs={"class": "form-control"}),
            "equipment": forms.SelectMultiple(attrs={"class": "form-control"})
        }
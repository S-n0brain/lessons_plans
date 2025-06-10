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
        
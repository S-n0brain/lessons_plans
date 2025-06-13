from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import LessonPlan, LessonStepTemplate
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from urllib.request import Request
from .forms import LessonPlanFileUploadForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse

from docx.section import Section
from docx import Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.enum.section import WD_ORIENT
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO


def generate_plan_lesson_word(lesson_plan):
    """
    Генерация документа word плана-конспекта урока с таблицей и информацией об уроке
    """
    steps_lesson = get_lesson_plan_steps(lesson_plan)
    document: Document = Document()
    section = get_section(document, 0)
    set_section_horizontal_orient(section)

    heading = gat_heading_lvl_0(document, 'План-конспект урока', 0)
    set_paragraph_alignment(heading, WD_ALIGN_PARAGRAPH.CENTER)

    set_document_font_name(document, "Times New Roman")
    set_paragraph_line_spacing(document.paragraphs[0], 1.5)

    lesson_fields = {"Предмет": lesson_plan.subject.name,
                     "Тема урока": lesson_plan.topic,
                     "Тип урока": lesson_plan.subject_type.name,
                     "Класс": lesson_plan.grade.name,
                     "Цель урока": lesson_plan.goal,
                     "Оборудование": lesson_plan.equipment.name}

    for i, field in enumerate(lesson_fields, 1):
        if lesson_fields[field]:
            document.add_paragraph(f"{field}: {lesson_fields[field]}")
            document.paragraphs[i].runs[0].font.size = Pt(14)
            document.paragraphs[i].runs[0].font.bold = True

    table_rows = len(steps_lesson) + 1
    table = get_table_document(document, rows_count=table_rows, columns_count=3)
    table.style = 'Table Grid'

    table.columns[0].width = section.page_width // 3 // 2
    table.columns[1].width = int((section.page_width - table.columns[0].width) / 2.5)
    table.columns[2].width = int((section.page_width - table.columns[0].width) / 2.5)

    hdr_cells = get_head_table(table)
    head_table_cells_text = ('Этап урока', 'Деятельность учителя', 'Деятельность обучающихся')
    set_style_head_table_lesson_plan(hdr_cells, head_table_cells_text)
    set_text_column_steps_lesson(table, steps_lesson)

    buffer = BytesIO()
    save_document_in_buffer(document, buffer)
    filename = f"lesson_plan_{lesson_plan.pk}.docx"
    django_file = ContentFile(buffer.read(), filename)
    lesson_plan.plan_file.save(filename, django_file)


def get_lesson_plan_steps(lesson_plan: LessonPlan) -> QuerySet:
    return LessonStepTemplate.object_step.filter(lesson_type=lesson_plan.subject_type).order_by("order")


def get_section(document: Document, num: int) -> Section:
    return document.sections[num]


def set_section_horizontal_orient(section: Section) -> None:
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11.69)  # ~A4 в альбомной (297 мм)
    section.page_height = Inches(8.27)  # ~A4 в портретной (210 мм)


def gat_heading_lvl_0(document: Document, text, level) -> Paragraph:
    return document.add_heading(text, level)


def set_paragraph_alignment(paragraph: Paragraph, alignment) -> None:
    paragraph.paragraph_format.alignment = alignment


def set_document_font_name(document: Document, font_name: str) -> None:
    document.paragraphs[0].runs[0].font.name = font_name


def set_paragraph_line_spacing(paragraph: Paragraph, line_spacing: float | int) -> None:
    paragraph.paragraph_format.line_spacing = line_spacing


def get_table_document(document, rows_count: int, columns_count: int) -> Table:
    return document.add_table(rows=rows_count, cols=columns_count)


def get_head_table(table: Table) -> tuple[_Cell]:
    return table.rows[0].cells


def set_style_head_table_lesson_plan(head: tuple[_Cell], head_cells_text: tuple[str, ...]) -> None:
    for i, text in enumerate(head_cells_text):
        head[i].text = text
        head_paragraph: Paragraph = head[i].paragraphs[0]
        set_paragraph_alignment(head_paragraph, WD_ALIGN_PARAGRAPH.CENTER)
        set_paragraph_line_spacing(head_paragraph, 1)
        head_paragraph.runs[0].font.bold = True
        head_paragraph.runs[0].font.size = Pt(12)


def set_text_column_steps_lesson(table: Table, steps_lesson: QuerySet) -> None:
    for i, step in enumerate(steps_lesson, 1):
        table.rows[i].cells[0].text = f"{i}. {step.name}"


def save_document_in_buffer(document: Document, buffer: BytesIO) -> None:
    document.save(buffer)
    buffer.seek(0)


class LessonPlanListView(ListView):
    model = LessonPlan
    template_name = "lesson_planner/index.html"
    extra_context = {"title": "Главная страница"}
    context_object_name = "lesson_plans"
    paginate_by = 6


class LessonPlanDetailView(FormMixin, DetailView):
    model = LessonPlan
    context_object_name = "lesson_plan"
    template_name = "lesson_planner/lessonplan_detail.html"
    form_class = LessonPlanFileUploadForm

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "План урока"
        context['form'] = LessonPlanFileUploadForm(instance=self.object)
        return context

    def post(self,  request: Request, *args, **kwargs):
        self.object : LessonPlan = self.get_object()
        action = request.POST.get("action")

        if action == "generate":
            generate_plan_lesson_word(lesson_plan=self.object)
            return redirect(self.object.get_absolute_url())
        elif action == "upload":
            form = LessonPlanFileUploadForm(request.POST, request.FILES, instance=self.object)
            if form.is_valid():
                form.save()
                return redirect(self.object.get_absolute_url())
        return self.get(request, args, kwargs)


class LessonPlanCreateView(CreateView):
    model = LessonPlan
    fields = "__all__"
    success_url = reverse_lazy("lesson_planner:index")


class LessonPlanDeleteView(DeleteView):
    model = LessonPlan
    success_url = reverse_lazy("lesson_planner:index")

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object : LessonPlan = self.get_object()
        self.object.delete()
        return redirect(self.success_url)


class LessonPlanUpdateView(UpdateView):
    model = LessonPlan
    fields = "__all__"

    def get_success_url(self):
        return reverse("lesson_planner:lesson_detail", args=[self.object.pk])

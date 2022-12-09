from django.shortcuts import render, redirect
from .forms import RegisterForm, ResumeForm
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import ResumeData

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


@login_required(login_url="/login")
def home(request):
    resumes = ResumeData.objects.filter(user=request.user)
    return render(request, 'main/home.html', {"resumes": resumes})


@login_required(login_url="/login")
def edit_resume(request):
    resume_data = ResumeData.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("/home")
    else:
        form = ResumeForm()

    return render(request, 'main/edit_resume.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def export_pdf(request):
    try:
        resume_data = ResumeData.objects.filter(user=request.user).first()
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        # Text object
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        lines = [
            f'Name: {resume_data.first_name} {resume_data.last_name}',
            f'Location: {resume_data.location}',
            '',
            f'Experience: {resume_data.experience}']

        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='resume.pdf')

    except ObjectDoesNotExist:
        return home(request)


from django.shortcuts import render, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .forms import ResumeUploadForm, KeywordForm
from .models import Resume, Employee
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .forms import ResumeUploadForm, KeywordForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Resume, Employee
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'resume_manager/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'resume_manager/signup.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('login')

# Add login_required to your main views
@login_required
def homepage(request):
  
    total_resumes = Resume.objects.count()
    total_employees = Employee.objects.count()
    
    return render(request, 'resume_manager/homepage.html', {
        'total_resumes': total_resumes,
        'total_employees': total_employees
    })


@login_required

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        
        # Skip form validation for multiple files and handle manually
        files = request.FILES.getlist('files')  # Get all files
        
        if files:  # If files were uploaded
            for f in files:
                Resume.objects.create(file=f)
            return redirect('resume_list')
        else:
            # No files selected
            form.add_error('files', 'Please select at least one file')
    else:
        form = ResumeUploadForm()
    
    return render(request, 'resume_manager/resume_upload.html', {'form': form})
@login_required

def resume_list(request):
    resumes = Resume.objects.all().order_by('-uploaded_at')
    return render(request, 'resume_manager/resume_list.html', {'resumes': resumes})

@login_required

def upload_and_rank(request):
    """Combines upload + keyword input + ranking in one flow"""
    # This can simply redirect to the existing upload_resume
    return redirect('upload_resume')

@login_required

def keyword_input(request):
    """Get keywords from user for ranking"""
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            # Store keywords in session for ranking
            request.session['search_keywords'] = [k.strip().lower() for k in keywords.split(',')]
            return redirect('rank_resumes')  # We'll create this
    else:
        form = KeywordForm()
    
    return render(request, 'resume_manager/keyword_input.html', {'form': form})

@login_required

def rank_resumes(request):
    """Scan resumes and rank them based on NLP (TF-IDF + Cosine Similarity)"""
    keywords = request.session.get('search_keywords', [])
    resumes = Resume.objects.all()
    
    if not keywords:
        return render(request, 'resume_manager/ranked_list.html', {
            'ranked_resumes': [],
            'keywords': [],
            'error': 'No keywords provided.'
        })
    
    keyword_query = " ".join(keywords).lower()
    resume_texts, resume_objs = [], []

    # Read resume contents
    for resume in resumes:
        try:
            content = resume.file.read().decode('utf-8').lower()
            resume_texts.append(content)
            resume_objs.append(resume)
            resume.file.seek(0)
        except:
            resume_texts.append("")
            resume_objs.append(resume)

    # TF-IDF and similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([keyword_query] + resume_texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Build ranked_resumes list (same as your structure)
    ranked_resumes = []
    for resume, score in zip(resume_objs, similarities):
        ranked_resumes.append({
            'resume': resume,
            'score': round(float(score) * 100, 2),  # percentage
            'matched_keywords': get_matched_keywords(resume, keywords)
        })

    # Sort descending by score
    ranked_resumes.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'resume_manager/ranked_list.html', {
        'ranked_resumes': ranked_resumes,
        'keywords': keywords
    })


def get_matched_keywords(resume, keywords):
    """Return which keywords appear in resume text"""
    try:
        text = resume.file.read().decode('utf-8').lower()
        resume.file.seek(0)
        return [kw for kw in keywords if kw.lower() in text]
    except:
        return []
    

@login_required

def manage_employees(request):
    """CRUD operations on hired employees"""
    employees = Employee.objects.all()
    return render(request, 'resume_manager/manage_employees.html', {'employees': employees})

@login_required

def hire_candidate(request, resume_id):
    """Move a candidate from resumes to employees"""
    resume = Resume.objects.get(id=resume_id)
    Employee.objects.create(
        name=resume.candidate_name(),
        resume=resume,
        skills=", ".join(get_matched_keywords(resume, [])),  # Will update after ranking
        score=0  # Will update after ranking
    )
    return redirect('manage_employees')


@login_required

def delete_employee(request, employee_id):
    """Delete an employee"""
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('manage_employees')


def delete_resume(request, resume_id):
    """Delete a resume"""
    resume = Resume.objects.get(id=resume_id)
    resume.delete()
    return redirect('resume_list')

@login_required
def edit_employee_name(request, employee_id):
    """Edit employee name"""
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            employee.name = new_name
            employee.save()
    return redirect('manage_employees')

@login_required
def edit_employee_skills(request, employee_id):
    """Edit employee skills"""
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        new_skills = request.POST.get('skills')
        if new_skills is not None:
            employee.skills = new_skills
            employee.save()
    return redirect('manage_employees')
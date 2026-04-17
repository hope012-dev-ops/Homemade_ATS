import re
import nltk
from collections import Counter

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

TECHNICAL_KEYWORDS = {
    'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'typescript'],
    'web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'asp.net', 'rest', 'api', 'graphql'],
    'data': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit', 'data analysis', 'data science', 'big data', 'hadoop', 'spark', 'etl'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'devops', 'jenkins'],
    'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'nosql', 'sql'],
    'tools': ['git', 'github', 'jira', 'agile', 'scrum', 'linux', 'unix', 'bash', 'shell'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical', 'management', 'project management', 'presentation', 'strategic']
}

def extract_skills(text):
    text_lower = text.lower()
    found_skills = {'technical': [], 'soft': []}
    
    for category, skills in TECHNICAL_KEYWORDS.items():
        for skill in skills:
            if skill in text_lower:
                if category == 'soft_skills':
                    if skill not in found_skills['soft']:
                        found_skills['soft'].append(skill)
                else:
                    if skill not in found_skills['technical']:
                        found_skills['technical'].append(skill)
    
    return found_skills

def extract_achievements(text):
    achievements = []
    
    number_patterns = [
        r'(\d+%)\s+(?:increase|decrease|growth|reduction|improvement)',
        r'(?:increased|decreased|grew|reduced|improved|achieved)\s+by\s+(\d+%)',
        r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
        r'(\d+)\s+(?:years?|months?|years\s+of)\s+(?:experience|working)',
        r'managed\s+(\d+)\s+(?:people|team|employees)',
        r'(\d+)\s+(?:clients|customers|projects)',
    ]
    
    for pattern in number_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        achievements.extend(matches)
    
    achievement_keywords = [
        'led', 'managed', 'developed', 'created', 'designed', 'implemented',
        'optimized', 'improved', 'increased', 'reduced', 'achieved',
        'awarded', 'recognized', 'certified', 'published', 'presented'
    ]
    
    sentences = re.split(r'[.!?\n]', text)
    for sentence in sentences:
        sentence = sentence.strip()
        if any(kw in sentence.lower() for kw in achievement_keywords):
            if len(sentence) > 20 and len(sentence) < 200:
                achievements.append(sentence)
    
    return achievements[:10]

def extract_experience(text):
    experience = []
    
    exp_section = re.search(r'(?:experience|work history|employment)(.*?)(?:education|skills|projects|$)', text, re.IGNORECASE | re.DOTALL)
    
    if exp_section:
        exp_text = exp_section.group(1)
        
        job_pattern = r'(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\s*[-–—to]+\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?[a-z]*\s*\d{0,4}|present|current)'
        
        jobs = re.split(job_pattern, exp_text, flags=re.IGNORECASE)
        
        for job in jobs:
            job = job.strip()
            if len(job) > 20 and len(job) < 300:
                experience.append(job)
    
    return experience[:5]

def extract_education(text):
    education = []
    
    edu_section = re.search(r'(?:education|academic|qualification)(.*?)(?:experience|skills|projects|$)', text, re.IGNORECASE | re.DOTALL)
    
    if edu_section:
        edu_text = edu_section.group(1)
        
        degree_pattern = r'(?:bachelor|master|phd|doctorate|associate|diploma|certificate)[^\.]*'
        degrees = re.findall(degree_pattern, edu_text, re.IGNORECASE)
        
        for degree in degrees:
            degree = degree.strip()
            if len(degree) > 5 and len(degree) < 150:
                education.append(degree)
    else:
        degree_pattern = r'(?:bachelor|master|phd|doctorate|associate|diploma|certificate)[^\.]*'
        degrees = re.findall(degree_pattern, text, re.IGNORECASE)
        education = [d.strip() for d in degrees if len(d.strip()) > 5][:5]
    
    return education

def extract_selling_points(text):
    result = {
        'skills': extract_skills(text),
        'achievements': extract_achievements(text),
        'experience': extract_experience(text),
        'education': extract_education(text),
        'highlights': []
    }
    
    if result['skills']['technical']:
        result['highlights'].append({
            'type': 'technical',
            'text': f"Strong technical skills in {', '.join(result['skills']['technical'][:5])}"
        })
    
    if result['achievements']:
        result['highlights'].append({
            'type': 'achievement',
            'text': f"Demonstrated {len(result['achievements'])} quantifiable achievements"
        })
    
    if result['experience']:
        result['highlights'].append({
            'type': 'experience',
            'text': f"Has {len(result['experience'])} documented work experiences"
        })
    
    if result['skills']['soft']:
        result['highlights'].append({
            'type': 'soft_skills',
            'text': f"Key soft skills: {', '.join(result['skills']['soft'][:3])}"
        })
    
    return result
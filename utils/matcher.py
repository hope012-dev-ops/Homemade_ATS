import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Remote",
        "type": "Full-time",
        "description": "We are looking for a Software Engineer to join our team. You will be responsible for developing and maintaining software applications. Proficiency in Python, JavaScript, and SQL is required. Experience with web frameworks like React or Django is a plus.",
        "required_skills": ["python", "javascript", "sql", "react", "django", "git", "html", "css", "api"],
        "soft_skills": ["communication", "problem-solving", "teamwork"]
    },
    {
        "id": 2,
        "title": "Data Scientist",
        "company": "Data Insights Inc",
        "location": "New York, NY",
        "type": "Full-time",
        "description": "Join our data science team to analyze complex datasets and build predictive models. Must have experience with machine learning, Python, and SQL. Knowledge of TensorFlow or PyTorch is preferred.",
        "required_skills": ["python", "machine learning", "sql", "tensorflow", "pytorch", "pandas", "numpy", "data analysis", "statistics"],
        "soft_skills": ["analytical", "communication", "problem-solving"]
    },
    {
        "id": 3,
        "title": "Frontend Developer",
        "company": "Web Solutions",
        "location": "San Francisco, CA",
        "type": "Full-time",
        "description": "Looking for a Frontend Developer with expertise in React, TypeScript, and CSS. You will be building responsive web applications and working closely with designers.",
        "required_skills": ["react", "javascript", "typescript", "html", "css", "redux", "responsive design", "git"],
        "soft_skills": ["creativity", "teamwork", "communication"]
    },
    {
        "id": 4,
        "title": "Backend Developer",
        "company": "API Systems",
        "location": "Austin, TX",
        "type": "Full-time",
        "description": "We need a Backend Developer to design and implement server-side logic. Experience with Node.js, Python, and database design is required. Knowledge of RESTful APIs and cloud services is a plus.",
        "required_skills": ["python", "node", "sql", "mongodb", "docker", "api", "rest", "aws", "git"],
        "soft_skills": ["problem-solving", "teamwork", "communication"]
    },
    {
        "id": 5,
        "title": "DevOps Engineer",
        "company": "CloudFirst",
        "location": "Seattle, WA",
        "type": "Full-time",
        "description": "Seeking a DevOps Engineer to manage CI/CD pipelines and cloud infrastructure. Experience with AWS, Kubernetes, Docker, and Terraform is required. Strong scripting skills needed.",
        "required_skills": ["aws", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "linux", "bash", "python"],
        "soft_skills": ["analytical", "problem-solving", "communication"]
    },
    {
        "id": 6,
        "title": "Product Manager",
        "company": "Innovation Labs",
        "location": "Boston, MA",
        "type": "Full-time",
        "description": "Looking for a Product Manager to lead product development. You will work with engineering and design teams to define product roadmaps. Experience with agile methodologies and data analysis is required.",
        "required_skills": ["agile", "scrum", "data analysis", "product management", "jira", "communication"],
        "soft_skills": ["leadership", "communication", "strategic", "teamwork"]
    },
    {
        "id": 7,
        "title": "Full Stack Developer",
        "company": "Digital Agency",
        "location": "Chicago, IL",
        "type": "Full-time",
        "description": "Join our team as a Full Stack Developer. You will work on both frontend and backend development. Proficiency in JavaScript, Python, and SQL is required. Experience with React and Node.js preferred.",
        "required_skills": ["javascript", "python", "sql", "react", "node", "html", "css", "api", "rest", "git"],
        "soft_skills": ["problem-solving", "teamwork", "communication"]
    },
    {
        "id": 8,
        "title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "Palo Alto, CA",
        "type": "Full-time",
        "description": "We are looking for a Machine Learning Engineer to develop and deploy ML models. Experience with TensorFlow, PyTorch, and cloud platforms is required. Strong background in deep learning and NLP preferred.",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "nlp", "docker", "aws", "sql"],
        "soft_skills": ["analytical", "problem-solving", "communication"]
    },
    {
        "id": 9,
        "title": "Data Analyst",
        "company": "Business Intelligence Co",
        "location": "Denver, CO",
        "type": "Full-time",
        "description": "Looking for a Data Analyst to analyze business data and create reports. Proficiency in SQL, Excel, and Tableau is required. Experience with Python and statistical analysis is a plus.",
        "required_skills": ["sql", "excel", "tableau", "python", "data analysis", "statistics", "pandas", "visualization"],
        "soft_skills": ["analytical", "communication", "presentation"]
    },
    {
        "id": 10,
        "title": "Cloud Architect",
        "company": "Enterprise Solutions",
        "location": "Washington, DC",
        "type": "Full-time",
        "description": "Seeking a Cloud Architect to design cloud infrastructure solutions. Experience with AWS, Azure, or GCP required. Strong knowledge of networking, security, and DevOps practices needed.",
        "required_skills": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "networking", "security", "devops"],
        "soft_skills": ["analytical", "leadership", "communication"]
    },
    {
        "id": 11,
        "title": "UI/UX Designer",
        "company": "Creative Studio",
        "location": "Los Angeles, CA",
        "type": "Full-time",
        "description": "Looking for a UI/UX Designer to create user-friendly interfaces. Experience with Figma, Sketch, and user research is required. Knowledge of HTML/CSS is a plus.",
        "required_skills": ["figma", "sketch", "ui design", "ux design", "prototyping", "user research", "html", "css"],
        "soft_skills": ["creativity", "communication", "problem-solving"]
    },
    {
        "id": 12,
        "title": "QA Engineer",
        "company": "Quality First",
        "location": "Portland, OR",
        "type": "Full-time",
        "description": "Join our QA team to ensure software quality. Experience with manual and automated testing is required. Knowledge of Selenium, Python, and agile methodologies is preferred.",
        "required_skills": ["selenium", "python", "testing", "automation", "agile", "jira", "git", "sql"],
        "soft_skills": ["analytical", "detail-oriented", "communication"]
    }
]

class JobMatcher:
    def __init__(self, jobs=None):
        self.jobs = jobs if jobs else SAMPLE_JOBS
    
    def _get_all_skills(self):
        all_skills = set()
        for job in self.jobs:
            all_skills.update(job['required_skills'])
            all_skills.update(job.get('soft_skills', []))
        return list(all_skills)
    
    def _calculate_skill_match(self, resume_skills, job_skills):
        if not resume_skills or not job_skills:
            return 0, [], []
        
        resume_set = set([s.lower() for s in resume_skills])
        job_set = set([s.lower() for s in job_skills])
        
        matched = list(resume_set.intersection(job_set))
        missing = list(job_set - resume_set)
        extra = list(resume_set - job_set)
        
        if not job_set:
            return 0, matched, missing
        
        match_percentage = (len(matched) / len(job_set)) * 100
        return round(match_percentage, 1), matched, missing
    
    def _calculate_text_similarity(self, resume_text, job_description):
        try:
            tfidf = TfidfVectorizer(stop_words='english')
            
            documents = [resume_text, job_description]
            tfidf_matrix = tfidf.fit_transform(documents)
            
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(similarity * 100, 1)
        except:
            return 0
    
    def match_jobs(self, resume_data, top_n=5):
        results = []
        
        resume_text = resume_data.get('text', '')
        technical_skills = resume_data.get('skills', {}).get('technical', [])
        soft_skills = resume_data.get('skills', {}).get('soft', [])
        all_resume_skills = technical_skills + soft_skills
        
        for job in self.jobs:
            tech_score, tech_matched, tech_missing = self._calculate_skill_match(
                technical_skills, job['required_skills']
            )
            
            soft_score, soft_matched, soft_missing = self._calculate_skill_match(
                soft_skills, job.get('soft_skills', [])
            )
            
            text_similarity = self._calculate_text_similarity(resume_text, job['description'])
            
            if tech_score > 0 or soft_score > 0:
                overall_score = (tech_score * 0.7) + (soft_score * 0.3)
            else:
                overall_score = text_similarity * 0.5
            
            results.append({
                'id': job['id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'type': job['type'],
                'score': round(overall_score, 1),
                'technical': {
                    'score': tech_score,
                    'matched': tech_matched,
                    'missing': tech_missing[:5]
                },
                'soft': {
                    'score': soft_score,
                    'matched': soft_matched,
                    'missing': soft_missing[:3]
                },
                'text_similarity': text_similarity
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_n]

def get_job_matcher():
    return JobMatcher(SAMPLE_JOBS)
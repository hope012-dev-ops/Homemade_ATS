CAREER_PATHS = {
    'software_development': {
        'title': 'Software Development',
        'roles': ['Junior Developer', 'Mid-Level Developer', 'Senior Developer', 'Lead Developer', 'Staff Engineer', 'Principal Engineer'],
        'skills_to_add': {
            'Junior Developer': ['git', 'docker', 'sql', 'rest api'],
            'Mid-Level Developer': ['ci/cd', 'testing', 'agile', 'system design'],
            'Senior Developer': ['architecture', 'mentoring', 'code review', 'performance optimization']
        },
        'description': 'Build and maintain software applications'
    },
    'data_science': {
        'title': 'Data Science & Analytics',
        'roles': ['Junior Data Analyst', 'Data Analyst', 'Data Scientist', 'Senior Data Scientist', 'ML Engineer', 'ML Lead'],
        'skills_to_add': {
            'Junior Data Analyst': ['excel', 'tableau', 'sql', 'python'],
            'Data Analyst': ['statistics', 'pandas', 'data visualization', 'powerbi'],
            'Data Scientist': ['machine learning', 'tensorflow', 'deep learning', 'nlp'],
            'ML Engineer': ['pytorch', 'mlops', 'kubernetes', 'cloud ml']
        },
        'description': 'Analyze data and build predictive models'
    },
    'devops': {
        'title': 'DevOps & Cloud Engineering',
        'roles': ['Junior DevOps', 'DevOps Engineer', 'Senior DevOps', 'Cloud Architect', 'SRE Lead'],
        'skills_to_add': {
            'Junior DevOps': ['linux', 'git', 'docker', 'aws basics'],
            'DevOps Engineer': ['kubernetes', 'terraform', 'jenkins', 'monitoring'],
            'Cloud Architect': ['multi-cloud', 'security', 'networking', 'cost optimization']
        },
        'description': 'Automate infrastructure and deployment pipelines'
    },
    'frontend': {
        'title': 'Frontend Development',
        'roles': ['Junior Frontend', 'Frontend Developer', 'Senior Frontend', 'UI/UX Engineer', 'Frontend Lead'],
        'skills_to_add': {
            'Junior Frontend': ['html', 'css', 'javascript', 'git'],
            'Frontend Developer': ['react', 'typescript', 'responsive design', 'webpack'],
            'Senior Frontend': ['performance', 'accessibility', 'state management', 'testing']
        },
        'description': 'Build user interfaces and web applications'
    },
    'backend': {
        'title': 'Backend Development',
        'roles': ['Junior Backend', 'Backend Developer', 'Senior Backend', 'Backend Lead', 'Systems Architect'],
        'skills_to_add': {
            'Junior Backend': ['python', 'sql', 'git', 'rest api'],
            'Backend Developer': ['database design', 'caching', 'message queues', 'testing'],
            'Backend Lead': ['microservices', 'api design', 'security', 'scalability']
        },
        'description': 'Build server-side applications and APIs'
    },
    'product_management': {
        'title': 'Product Management',
        'roles': ['Associate PM', 'Product Manager', 'Senior PM', 'Group PM', 'Director of Product'],
        'skills_to_add': {
            'Associate PM': ['jira', 'agile', 'user research', 'sql basics'],
            'Product Manager': ['roadmapping', 'data analysis', 'stakeholder management', 'a/b testing'],
            'Senior PM': ['strategy', ' OKRs', 'mentoring', 'cross-functional leadership']
        },
        'description': 'Define and drive product strategy'
    },
    'qa': {
        'title': 'Quality Assurance',
        'roles': ['Junior QA', 'QA Engineer', 'Senior QA', 'QA Lead', 'Test Automation Lead'],
        'skills_to_add': {
            'Junior QA': ['manual testing', 'test cases', 'jira', 'bug tracking'],
            'QA Engineer': ['selenium', 'api testing', 'sql', 'test planning'],
            'QA Lead': ['test automation frameworks', 'ci/cd', 'performance testing', 'security testing']
        },
        'description': 'Ensure software quality and reliability'
    },
    'cybersecurity': {
        'title': 'Cybersecurity',
        'roles': ['Security Analyst', 'Security Engineer', 'Senior Security Engineer', 'Security Architect', 'CISO'],
        'skills_to_add': {
            'Security Analyst': ['networking', 'linux', 'siem', 'firewall'],
            'Security Engineer': ['penetration testing', 'vulnerability assessment', 'incident response', 'coding'],
            'Security Architect': ['zero trust', 'cloud security', 'compliance', 'risk assessment']
        },
        'description': 'Protect systems and data from threats'
    }
}

SKILL_CATEGORIES = {
    'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'typescript'],
    'web_frameworks': ['react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'next.js', 'express'],
    'data_ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'sql', 'tableau', 'powerbi'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'serverless'],
    'devops': ['ci/cd', 'jenkins', 'gitlab', 'ansible', 'linux', 'bash', 'git'],
    'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'nosql', 'elasticsearch'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical', 'management', 'agile', 'scrum'],
    'tools': ['jira', 'confluence', 'figma', 'git', 'docker', 'linux']
}

def analyze_career_path(resume_data):
    text = resume_data.get('text', '').lower()
    skills = resume_data.get('skills', {})
    technical_skills = [s.lower() for s in skills.get('technical', [])]
    soft_skills = [s.lower() for s in skills.get('soft', [])]
    
    matched_paths = []
    recommended_skills = set()
    
    for path_key, path_data in CAREER_PATHS.items():
        match_score = 0
        path_skills = []
        
        for category, category_skills in SKILL_CATEGORIES.items():
            for skill in technical_skills:
                if skill in category_skills:
                    path_skills.append(skill)
                    match_score += 1
        
        if path_skills or match_score > 0:
            matched_paths.append({
                'path': path_key,
                'title': path_data['title'],
                'description': path_data['description'],
                'score': min(match_score * 15, 85),
                'current_skills': path_skills[:5],
                'roles': path_data['roles']
            })
    
    for path in matched_paths:
        role_idx = 0
        if path['score'] > 60:
            role_idx = 2
        elif path['score'] > 30:
            role_idx = 1
        
        current_role = path['roles'][role_idx] if role_idx < len(path['roles']) else path['roles'][0]
        next_role = path['roles'][role_idx + 1] if role_idx + 1 < len(path['roles']) else path['roles'][-1]
        
        skills_to_learn = path_data['skills_to_add'].get(current_role, [])
        
        path['current_role'] = current_role
        path['next_role'] = next_role
        path['skills_to_learn'] = skills_to_learn
        recommended_skills.update(skills_to_learn)
    
    matched_paths.sort(key=lambda x: x['score'], reverse=True)
    
    all_recommended = list(recommended_skills)[:10]
    
    return {
        'career_paths': matched_paths[:3],
        'recommended_skills': all_recommended,
        'summary': generate_career_summary(matched_paths)
    }

def generate_career_summary(paths):
    if not paths:
        return "Consider exploring roles in software development, data science, or product management based on your background."
    
    summary_parts = []
    for path in paths[:2]:
        summary_parts.append(f"{path['title']} ({path['score']:.0f}% match)")
    
    return "Based on your skills, consider: " + " | ".join(summary_parts)

def get_skill_recommendations(current_skills):
    recommendations = {
        'high_demand': [],
        'complementary': [],
        'emerging': []
    }
    
    high_demand_skills = ['python', 'aws', 'docker', 'kubernetes', 'react', 'sql', 'machine learning', 'typescript']
    emerging_skills = ['rust', 'go', 'graphql', 'mlops', 'edge computing', 'web3']
    
    for skill in high_demand_skills:
        if skill not in current_skills:
            recommendations['high_demand'].append(skill)
    
    for skill in emerging_skills:
        if skill not in current_skills:
            recommendations['emerging'].append(skill)
    
    return recommendations
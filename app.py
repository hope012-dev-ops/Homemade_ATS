import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from utils.parser import parse_resume, allowed_file
from utils.analyzer import ResumeAnalyzer
from utils.selling_points import extract_selling_points
from utils.matcher import get_job_matcher

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT, PNG, JPG, JPEG'}), 400
    
    try:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        parsed = parse_resume(filepath)
        
        analyzer = ResumeAnalyzer()
        grammar_errors = analyzer.check_grammar(parsed['text'])
        formatting_issues = analyzer.analyze_formatting(parsed['text'])
        suggestions = analyzer.suggest_fixes(parsed['text'], grammar_errors)
        
        selling_points = extract_selling_points(parsed['text'])
        
        if 'skills' not in parsed:
            parsed['skills'] = selling_points['skills']
        
        matcher = get_job_matcher()
        job_matches = matcher.match_jobs({
            'text': parsed['text'],
            'skills': selling_points['skills']
        })
        
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'data': {
                'name': parsed.get('name'),
                'contact': parsed.get('contact'),
                'text': parsed['text'],
                'word_count': parsed.get('word_count', 0),
                'grammar_errors': grammar_errors,
                'formatting_issues': formatting_issues,
                'suggestions': suggestions,
                'selling_points': selling_points,
                'job_matches': job_matches
            }
        })
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 10MB'}), 413
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
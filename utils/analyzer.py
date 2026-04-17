import re
import language_tool_python
from collections import Counter
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

class ResumeAnalyzer:
    def __init__(self):
        self.tool = None
    
    def _get_tool(self):
        if self.tool is None:
            self.tool = language_tool_python.LanguageTool('en-US')
        return self.tool
    
    def check_grammar(self, text):
        try:
            tool = self._get_tool()
            matches = tool.check(text)
            
            errors = []
            for match in matches:
                error_info = {
                    'type': self._categorize_error(match.rule_id),
                    'message': match.message,
                    'context': match.context,
                    'offset': match.offset,
                    'length': match.error_length,
                    'suggestions': match.replacements[:3] if match.replacements else []
                }
                errors.append(error_info)
            
            return errors
        except Exception as e:
            return [{'type': 'error', 'message': str(e), 'context': '', 'offset': 0, 'length': 0, 'suggestions': []}]
    
    def _categorize_error(self, rule_id):
        rule_id_lower = rule_id.lower()
        if 'spell' in rule_id_lower or 'typo' in rule_id_lower:
            return 'spelling'
        elif 'punct' in rule_id_lower:
            return 'punctuation'
        elif 'grammar' in rule_id_lower:
            return 'grammar'
        elif 'style' in rule_id_lower:
            return 'style'
        else:
            return 'grammar'
    
    def analyze_formatting(self, text):
        issues = []
        lines = text.split('\n')
        non_empty_lines = [l.strip() for l in lines if l.strip()]
        
        if len(non_empty_lines) < 5:
            issues.append({
                'type': 'length',
                'severity': 'warning',
                'message': 'Resume appears too short. Consider adding more detail.'
            })
        
        if len(text.split()) > 1500:
            issues.append({
                'type': 'length',
                'severity': 'warning',
                'message': 'Resume may be too long. Consider keeping it to 1-2 pages.'
            })
        
        required_sections = ['experience', 'education', 'skills']
        text_lower = text.lower()
        
        for section in required_sections:
            if section not in text_lower:
                issues.append({
                    'type': 'missing_section',
                    'severity': 'info',
                    'message': f'Consider adding a {section.title()} section.'
                })
        
        bullet_pattern = r'^[\s]*[-*•]\s'
        has_bullets = any(re.match(bullet_pattern, line) for line in lines)
        
        if not has_bullets:
            issues.append({
                'type': 'formatting',
                'severity': 'info',
                'message': 'Consider using bullet points for listing items.'
            })
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.search(email_pattern, text):
            issues.append({
                'type': 'missing_info',
                'severity': 'warning',
                'message': 'No email address found. Include your email for contact.'
            })
        
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        if not re.search(phone_pattern, text):
            issues.append({
                'type': 'missing_info',
                'severity': 'info',
                'message': 'No phone number found. Consider adding a contact number.'
            })
        
        return issues
    
    def suggest_fixes(self, text, grammar_errors):
        suggestions = []
        
        for error in grammar_errors:
            if error['suggestions']:
                suggestions.append({
                    'error': error['context']['text'] if 'text' in error['context'] else '',
                    'fix': error['suggestions'][0],
                    'type': error['type']
                })
        
        formatting_suggestions = [
            'Use action verbs at the beginning of bullet points (e.g., Led, Developed, Created)',
            'Quantify achievements where possible (e.g., "Increased sales by 25%")',
            'Use consistent formatting for dates (e.g., "Jan 2020 - Present")',
            'Keep your resume focused on relevant experience',
            'Use a clean, professional font like Arial or Calibri',
            'Ensure consistent indentation throughout'
        ]
        
        return {
            'grammar_suggestions': suggestions,
            'formatting_suggestions': formatting_suggestions
        }
# Resume Analyzer - Project Specification

## Project Overview
- **Project Name**: Resume Analyzer
- **Type**: Web Application (Python Flask + HTML/CSS/JS)
- **Core Functionality**: Upload resumes (PDF, DOCX, TXT, images), analyze content for grammar/formatting issues, identify selling points, and match with suitable job positions.
- **Target Users**: Job seekers looking to improve their resumes and find matching job opportunities.

## Technology Stack
- **Backend**: Python with Flask
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **File Processing**: PyMuPDF (PDF), python-docx (DOCX), pytesseract (OCR/images)
- **Grammar Check**: language_tool_python (LanguageTool wrapper)
- **NLP**: spaCy, NLTK for text processing
- **Job Matching**: TF-IDF + Cosine Similarity

## UI/UX Specification

### Layout Structure
- **Header**: Logo + Navigation (50px height)
- **Main Container**: Max-width 1200px, centered
- **Sections**:
  1. Upload Zone (drag & drop + file picker)
  2. Analysis Results (tabbed interface)
  3. Job Matches (card-based grid)
- **Responsive Breakpoints**: 
  - Mobile: < 768px (single column)
  - Tablet: 768-1024px (2 columns)
  - Desktop: > 1024px (3 columns for job cards)

### Visual Design
- **Color Palette**:
  - Primary: #2563EB (blue)
  - Secondary: #1E293B (dark slate)
  - Accent: #10B981 (emerald green for success)
  - Warning: #F59E0B (amber)
  - Error: #EF4444 (red)
  - Background: #F8FAFC (light gray)
  - Card Background: #FFFFFF
  - Text Primary: #0F172A
  - Text Secondary: #64748B

- **Typography**:
  - Font Family: 'Inter', system-ui, sans-serif
  - Headings: 700 weight, 24px (h1), 20px (h2), 16px (h3)
  - Body: 400 weight, 14px
  - Line height: 1.6

- **Spacing**: 8px base unit (8, 16, 24, 32, 48)
- **Border Radius**: 8px (cards), 6px (buttons), 4px (inputs)
- **Shadows**: 
  - Card: 0 1px 3px rgba(0,0,0,0.1)
  - Hover: 0 4px 12px rgba(0,0,0,0.15)

### Components
1. **Upload Zone**:
   - Dashed border (#CBD5E1), 2px
   - Icon: upload cloud
   - States: default, hover (blue border), dragover (blue bg), processing (pulse animation)

2. **Tab Navigation**:
   - Horizontal tabs: Resume Text | Grammar Analysis | Selling Points | Suggestions
   - Active: blue underline, bold text
   - Inactive: gray text

3. **Result Cards**:
   - White background, shadow on hover
   - Icons for each section
   - Collapsible content

4. **Job Match Cards**:
   - Job title, company, match percentage badge
   - Skills tags (matched in green, missing in amber)
   - "Apply" button linking to job search

5. **Grammar Error Items**:
   - Error type badge (Grammar/Spelling/Punctuation)
   - Error text highlighted
   - Suggestion in green

6. **Loading States**:
   - Spinner for processing
   - Progress bar for file upload
   - Skeleton loaders for results

### Animations
- Fade-in for results (0.3s ease)
- Slide-up for job cards (staggered 0.1s)
- Pulse on processing indicators
- Smooth tab transitions

## Functionality Specification

### 1. File Upload & Processing
- **Supported Formats**: PDF, DOCX, TXT, PNG, JPG, JPEG
- **Max File Size**: 10MB
- **Upload Methods**: Drag & drop, file picker
- **Processing**:
  - PDF: Extract text using PyMuPDF
  - DOCX: Extract using python-docx
  - TXT: Direct text read
  - Images: OCR via pytesseract

### 2. Grammar & Formatting Analysis
- **Grammar Errors**: Subject-verb agreement, tense, article usage
- **Spelling Errors**: Typos, misspellings
- **Punctuation**: Missing/incorrect punctuation
- **Formatting Checks**:
  - Section headers present (Experience, Education, Skills)
  - Consistent bullet formatting
  - Appropriate length (resume should be 1-2 pages)
  - Contact info present and properly formatted
- **Output**: List of errors with context, position, and suggested fixes

### 3. Selling Points Extraction
- **Key Achievements**: Numbers, results, metrics
- **Skills Identification**: Technical and soft skills
- **Experience Highlights**: Notable roles, responsibilities
- **Education**: Degrees, certifications
- **Keywords**: Industry-specific terms

### 4. Resume Suggestions
- Formatting improvements
- Content enhancements
- Missing sections detection
- Action verb suggestions
- Quantification suggestions for achievements

### 5. Job Matching
- **Sample Job Database**: Pre-defined list of job positions with required skills
- **Matching Algorithm**: 
  - TF-IDF vectorization for skills comparison
  - Cosine similarity scoring
  - Weighted scoring (technical skills 70%, soft skills 30%)
- **Output**: Ranked list of matching jobs with scores and match details

### 6. API Integration
- Use external resources for additional job data if available
- Grammar checking uses LanguageTool API (can run locally or remote)

## Acceptance Criteria
1. User can upload PDF, DOCX, TXT, or image files
2. Text is extracted and displayed in readable format
3. Grammar errors are identified with suggested fixes
4. Selling points are highlighted and listed
5. Formatting suggestions are provided
6. At least 10 sample jobs are available for matching
7. Job matches show percentage score and skill breakdown
8. UI is responsive and works on mobile
9. Processing shows loading state
10. Error handling for invalid files

## Project Structure
```
resume-analyzer/
├── app.py                 # Flask application
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css         # Styles
│   └── script.js         # Frontend logic
├── templates/
│   └── index.html        # Main HTML
├── utils/
│   ├── parser.py        # File parsing
│   ├── analyzer.py      # Grammar/format analysis
│   ├── matcher.py       # Job matching
│   └── jobs.json        # Sample job database
└── uploads/              # Temp upload folder
```
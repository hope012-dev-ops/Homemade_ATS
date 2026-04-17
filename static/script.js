document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const resultsSection = document.getElementById('resultsSection');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    const errorToast = document.getElementById('errorToast');
    const errorMessage = document.getElementById('errorMessage');
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    let isProcessing = false;

    // Upload zone events
    uploadZone.addEventListener('click', () => fileInput.click());
    
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        if (isProcessing) return;
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0 && !isProcessing) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // New analysis
    newAnalysisBtn.addEventListener('click', resetAnalysis);

    // Tab navigation
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `tab-${targetTab}`) {
                    content.classList.add('active');
                }
            });
        });
    });

    function handleFileUpload(file) {
        if (file.size > 10 * 1024 * 1024) {
            showError('File too large. Maximum size is 10MB.');
            return;
        }

        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'image/png', 'image/jpeg', 'image/jpg'];
        const allowedExtensions = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg'];
        
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(ext)) {
            showError('Invalid file type. Allowed: PDF, DOCX, TXT, PNG, JPG, JPEG');
            return;
        }

        startProcessing();
        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        simulateProgress();
        
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResults(data.data);
            } else {
                showError(data.error || 'An error occurred');
                resetAnalysis();
            }
        })
        .catch(error => {
            showError('Network error. Please try again.');
            resetAnalysis();
        });
    }

    function simulateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 200);

        window.progressInterval = interval;
    }

    function startProcessing() {
        isProcessing = true;
        uploadZone.style.display = 'none';
        uploadProgress.classList.add('active');
        progressFill.style.width = '0%';
    }

    function stopProcessing() {
        isProcessing = false;
        if (window.progressInterval) {
            clearInterval(window.progressInterval);
        }
        progressFill.style.width = '100%';
        setTimeout(() => {
            uploadProgress.classList.remove('active');
            uploadZone.style.display = 'block';
        }, 500);
    }

    function displayResults(data) {
        stopProcessing();
        
        // Word count
        document.getElementById('wordCount').textContent = `${data.word_count} words`;
        
        // Resume text
        document.getElementById('resumeText').textContent = data.text || 'No text extracted';
        
        // Grammar errors
        const errorsList = document.getElementById('errorsList');
        const errorCount = document.getElementById('errorCount');
        
        if (data.grammar_errors && data.grammar_errors.length > 0) {
            errorCount.textContent = `${data.grammar_errors.length} issues`;
            errorsList.innerHTML = data.grammar_errors.map(error => `
                <div class="error-item">
                    <span class="error-type">${error.type || 'Grammar'}</span>
                    <div class="error-content">
                        <p class="error-context">${escapeHtml(error.context || '')}</p>
                        <p class="error-suggestion">${escapeHtml(error.message || error.suggestion || '')}</p>
                    </div>
                </div>
            `).join('');
        } else {
            errorCount.textContent = '0 issues';
            errorCount.className = 'badge badge-success';
            errorsList.innerHTML = '<p style="color: var(--accent); text-align: center; padding: 20px;">No grammar errors found!</p>';
        }
        
        // Formatting issues
        const formattingIssues = document.getElementById('formattingIssues');
        if (data.formatting_issues && data.formatting_issues.length > 0) {
            formattingIssues.innerHTML = data.formatting_issues.map(issue => `
                <div class="formatting-item">
                    <svg class="formatting-icon ${issue.status === 'good' ? 'success' : 'warning'}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        ${issue.status === 'good' 
                            ? '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>'
                            : '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>'}
                    </svg>
                    <span class="formatting-text">${escapeHtml(issue.message)}</span>
                </div>
            `).join('');
        } else {
            formattingIssues.innerHTML = '<p style="color: var(--accent); text-align: center; padding: 20px;">Resume looks well formatted!</p>';
        }
        
        // Selling points
        const sellingPoints = document.getElementById('sellingPoints');
        const sp = data.selling_points;
        let spHtml = '';
        
        if (sp.achievements && sp.achievements.length > 0) {
            spHtml += `
                <div class="selling-category">
                    <h4>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                        </svg>
                        Key Achievements
                    </h4>
                    <div class="selling-items">
                        ${sp.achievements.map(a => `<span class="selling-tag highlight">${escapeHtml(a)}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (sp.skills && sp.skills.technical && sp.skills.technical.length > 0) {
            spHtml += `
                <div class="selling-category">
                    <h4>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="16 18 22 12 16 6"></polyline>
                            <polyline points="8 6 2 12 8 18"></polyline>
                        </svg>
                        Technical Skills
                    </h4>
                    <div class="selling-items">
                        ${sp.skills.technical.map(s => `<span class="selling-tag">${escapeHtml(s)}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (sp.skills && sp.skills.soft && sp.skills.soft.length > 0) {
            spHtml += `
                <div class="selling-category">
                    <h4>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                        Soft Skills
                    </h4>
                    <div class="selling-items">
                        ${sp.skills.soft.map(s => `<span class="selling-tag">${escapeHtml(s)}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (sp.experience && sp.experience.length > 0) {
            spHtml += `
                <div class="selling-category">
                    <h4>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                        </svg>
                        Experience Highlights
                    </h4>
                    <div class="selling-items">
                        ${sp.experience.map(e => `<span class="selling-tag">${escapeHtml(e)}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (sp.education && sp.education.length > 0) {
            spHtml += `
                <div class="selling-category">
                    <h4>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                            <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                        </svg>
                        Education
                    </h4>
                    <div class="selling-items">
                        ${sp.education.map(e => `<span class="selling-tag">${escapeHtml(e)}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (!spHtml) {
            spHtml = '<p style="text-align: center; padding: 20px; color: var(--text-secondary);">No selling points detected</p>';
        }
        
        sellingPoints.innerHTML = spHtml;
        
        // Suggestions
        const suggestionsList = document.getElementById('suggestionsList');
        if (data.suggestions && data.suggestions.length > 0) {
            suggestionsList.innerHTML = data.suggestions.map(suggestion => `
                <div class="suggestion-item">
                    <svg class="suggestion-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="16" x2="12" y2="12"></line>
                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    <div class="suggestion-content">
                        <h4>${escapeHtml(suggestion.type || 'Suggestion')}</h4>
                        <p>${escapeHtml(suggestion.message || suggestion)}</p>
                    </div>
                </div>
            `).join('');
        } else {
            suggestionsList.innerHTML = '<p style="text-align: center; padding: 20px; color: var(--accent);">Great job! Your resume looks solid.</p>';
        }
        
        // Career Path
        const careerPaths = document.getElementById('careerPaths');
        if (data.career_analysis && data.career_analysis.career_paths && data.career_analysis.career_paths.length > 0) {
            careerPaths.innerHTML = data.career_analysis.career_paths.map(path => `
                <div class="career-path-card">
                    <div class="career-path-header">
                        <h4>${escapeHtml(path.title)}</h4>
                        <span class="match-percentage">${path.score}%</span>
                    </div>
                    <p class="career-path-desc">${escapeHtml(path.description)}</p>
                    <div class="career-path-roles">
                        <span class="role-current">Current: ${escapeHtml(path.current_role)}</span>
                        <span class="role-arrow">→</span>
                        <span class="role-next">Next: ${escapeHtml(path.next_role)}</span>
                    </div>
                    <div class="skills-to-learn">
                        <h5>Skills to Learn:</h5>
                        <div class="skills-list">
                            ${path.skills_to_learn.map(s => `<span class="skill-tag recommended">${escapeHtml(s)}</span>`).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            careerPaths.innerHTML = '<p style="text-align: center; padding: 20px; color: var(--text-secondary);">Upload a resume to see career path recommendations</p>';
        }
        
        // Skill Upgrades
        const skillUpgrades = document.getElementById('skillUpgrades');
        const rec = data.skill_recommendations;
        if (rec && (rec.high_demand?.length > 0 || rec.complementary?.length > 0 || rec.emerging?.length > 0)) {
            let upgradesHtml = '';
            
            if (rec.high_demand && rec.high_demand.length > 0) {
                upgradesHtml += `
                    <div class="skill-category">
                        <h4>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                            </svg>
                            High Demand Skills
                        </h4>
                        <p>These skills are frequently requested by employers</p>
                        <div class="skills-list">
                            ${rec.high_demand.map(s => `<span class="skill-tag recommended">${escapeHtml(s)}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            
            if (rec.emerging && rec.emerging.length > 0) {
                upgradesHtml += `
                    <div class="skill-category">
                        <h4>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                            </svg>
                            Emerging Technologies
                        </h4>
                        <p>Skills gaining traction in the industry</p>
                        <div class="skills-list">
                            ${rec.emerging.map(s => `<span class="skill-tag emerging">${escapeHtml(s)}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            
            skillUpgrades.innerHTML = upgradesHtml;
        } else {
            skillUpgrades.innerHTML = '<p style="text-align: center; padding: 20px; color: var(--text-secondary);">No specific recommendations at this time</p>';
        }
        
        // Job matches
        const jobsGrid = document.getElementById('jobsGrid');
        if (data.job_matches && data.job_matches.length > 0) {
            jobsGrid.innerHTML = data.job_matches.map(job => `
                <div class="job-card">
                    <div class="job-header">
                        <div>
                            <h3 class="job-title">${escapeHtml(job.title)}</h3>
                            <p class="job-company">${escapeHtml(job.company)}</p>
                        </div>
                        <div class="job-score">
                            <span class="match-percentage">${job.score}%</span>
                            <span class="match-label">Match</span>
                        </div>
                    </div>
                    <div class="job-details">
                        <span class="job-detail">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            ${escapeHtml(job.location)}
                        </span>
                        <span class="job-detail">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                            </svg>
                            ${escapeHtml(job.type)}
                        </span>
                    </div>
                    <div class="job-skills">
                        <h5>Matched Skills</h5>
                        <div class="skills-matched">
                            ${job.technical.matched.map(s => `<span class="skill-tag">${escapeHtml(s)}</span>`).join('')}
                            ${job.soft.matched.map(s => `<span class="skill-tag">${escapeHtml(s)}</span>`).join('')}
                        </div>
                        ${job.technical.missing.length > 0 || job.soft.missing.length > 0 ? `
                            <h5>Missing Skills</h5>
                            <div class="skills-missing">
                                ${job.technical.missing.map(s => `<span class="skill-tag missing">${escapeHtml(s)}</span>`).join('')}
                                ${job.soft.missing.map(s => `<span class="skill-tag missing">${escapeHtml(s)}</span>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        } else {
            jobsGrid.innerHTML = '<p style="text-align: center; padding: 40px; color: var(--text-secondary); grid-column: 1/-1;">No matching jobs found. Try adding more skills to your resume!</p>';
        }
        
        // Show results
        resultsSection.classList.add('active');
        
        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    function resetAnalysis() {
        resultsSection.classList.remove('active');
        fileInput.value = '';
        
        // Reset tabs to first
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        tabs[0].classList.add('active');
        document.getElementById('tab-text').classList.add('active');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorToast.classList.add('active');
        
        setTimeout(() => {
            errorToast.classList.remove('active');
        }, 4000);
    }

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
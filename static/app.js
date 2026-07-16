(function() {
    'use strict';

    // Elements
    const themeToggle = document.getElementById('theme-toggle');
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    const loadingStage = document.getElementById('loading-stage');
    const error = document.getElementById('error');
    const newsletter = document.getElementById('newsletter');
    const newsletterContent = document.getElementById('newsletter-content');
    const newsletterDate = document.getElementById('newsletter-date');
    const emptyState = document.getElementById('empty-state');
    const regenerateLink = document.getElementById('regenerate-link');

    // Theme
    const THEME_KEY = 'newsletter-theme';
    function initTheme() {
        const saved = localStorage.getItem(THEME_KEY) || 'light';
        document.documentElement.setAttribute('data-theme', saved);
    }
    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem(THEME_KEY, next);
    }
    themeToggle.addEventListener('click', toggleTheme);
    initTheme();

    // Loading stages
    const stages = [
        'Generating search queries...',
        'Fetching articles from sources...',
        'Deduplicating articles...',
        'Filtering for FMCG deal relevance...',
        'Scoring source credibility...',
        'Generating structured newsletter...'
    ];
    let stageIndex = 0;
    let stageInterval;

    function startLoading() {
        stageIndex = 0;
        loadingStage.textContent = stages[0];
        loading.classList.remove('hidden');
        generateBtn.disabled = true;
        newsletter.classList.add('hidden');
        error.classList.add('hidden');
        emptyState.classList.add('hidden');
        stageInterval = setInterval(() => {
            stageIndex = (stageIndex + 1) % stages.length;
            loadingStage.textContent = stages[stageIndex];
        }, 2000);
    }

    function stopLoading() {
        clearInterval(stageInterval);
        loading.classList.add('hidden');
        generateBtn.disabled = false;
    }

    function formatDate() {
        const now = new Date();
        return now.toLocaleDateString('en-IN', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // Simple markdown to HTML converter
    function renderMarkdown(text) {
        if (!text) return '<p>No content available.</p>';

        let lines = text.split('\n');
        let html = '';
        let inList = false;
        let items = [];

        function flushList() {
            if (items.length > 0) {
                html += '<ul>\n' + items.join('\n') + '\n</ul>\n';
                items = [];
                inList = false;
            }
        }

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            let trimmed = line.trim();

            if (trimmed === '') {
                flushList();
                continue;
            }

            // Headings: ### Title or ## Title
            if (/^#{2,3}\s/.test(line)) {
                flushList();
                let tag = line.trim().startsWith('## ') ? 'h3' : 'h3';
                let content = line.replace(/^#{2,3}\s+/, '').trim();
                // Convert bold/italic inside heading
                content = content
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>');
                html += '<h3>' + content + '</h3>\n';
                continue;
            }

            // List item: - something
            if (/^-\s/.test(line)) {
                inList = true;
                let content = line.replace(/^-\s+/, '').trim();
                // Bold/italic
                content = content
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>');
                // Inline code
                content = content.replace(/`(.+?)`/g, '<code>$1</code>');
                items.push('  <li>' + content + '</li>');
                continue;
            }

            // Horizontal rule
            if (/^-{3,}$/.test(trimmed)) {
                flushList();
                html += '<hr>\n';
                continue;
            }

            // Paragraph
            flushList();
            let para = trimmed;
            para = para
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.+?)\*/g, '<em>$1</em>');
            html += '<p>' + para + '</p>\n';
        }

        flushList();
        return html;
    }

    function showNewsletter(html) {
        newsletterContent.innerHTML = renderMarkdown(html);
        newsletterDate.textContent = formatDate();
        newsletter.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    function showError(msg) {
        error.textContent = msg;
        error.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    async function generate() {
        startLoading();
        try {
            const res = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: 'ma-funding', region: 'india', date: 'today' })
            });
            const data = await res.json();
            stopLoading();
            if (data.success) {
                showNewsletter(data.html);
            } else {
                showError(data.error || 'Failed to generate newsletter');
            }
        } catch (err) {
            stopLoading();
            showError('Network error: ' + err.message);
        }
    }

    generateBtn.addEventListener('click', generate);
    regenerateLink.addEventListener('click', (e) => {
        e.preventDefault();
        generate();
    });

    async function checkStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            if (!data.ollama_running) {
                console.warn('Ollama not running - generation will fail');
            }
        } catch (e) {
            console.warn('Status check failed:', e);
        }
    }
    checkStatus();

})();
const PHASES = [
    { id: 1, name: "Research", role: "Senior Systems Analyst", model: "Codex" },
    { id: 2, name: "Analyze & Plan", role: "Lead Software Architect", model: "Codex" },
    { id: 2.5, name: "Plan Review", role: "Principal Architect", model: "Claude" },
    { id: 3, name: "Break Down Tasks", role: "Agile Scrum Master", model: "Gemini" },
    { id: 4, name: "Execute Code", role: "Senior Staff Engineer", model: "Codex" },
    { id: 5, name: "Test & Validate", role: "Orchestrator", model: "Antigravity IDE" },
    { id: 6, name: "Code Audit", role: "Advisor / Security Auditor", model: "Claude" },
    { id: 7, name: "Final Report", role: "Technical Writer", model: "Gemini" }
];

function renderTimeline(currentPhase) {
    const timelineEl = document.getElementById('timeline');
    timelineEl.innerHTML = '';
    
    PHASES.forEach(phase => {
        const div = document.createElement('div');
        div.className = 'timeline-item';
        
        if (phase.id < currentPhase) {
            div.classList.add('completed');
        } else if (phase.id === currentPhase) {
            div.classList.add('active');
        }
        
        if (phase.id === 2.5) {
            div.classList.add('phase-2-5');
        }
        
        div.innerHTML = `
            <h3>Phase ${phase.id}: ${phase.name}</h3>
            <p>${phase.role} (${phase.model})</p>
        `;
        timelineEl.appendChild(div);
    });
}

function renderKanban(tasks) {
    const columns = {
        'todo': document.querySelector('#col-todo .column-content'),
        'in_progress': document.querySelector('#col-in_progress .column-content'),
        'in_test': document.querySelector('#col-in_test .column-content'),
        'stuck': document.querySelector('#col-stuck .column-content'),
        'done': document.querySelector('#col-done .column-content')
    };

    // Clear all columns
    Object.values(columns).forEach(col => col.innerHTML = '');

    if (!tasks || !tasks.length) return;

    tasks.forEach(task => {
        const status = task.status || 'todo';
        const targetCol = columns[status] || columns['todo'];

        const card = document.createElement('div');
        card.className = 'kanban-card';

        const titleEl = document.createElement('div');
        titleEl.className = 'card-title';
        titleEl.textContent = task.title || 'Untitled Task';
        card.appendChild(titleEl);

        const metaEl = document.createElement('div');
        metaEl.className = 'card-meta';

        const assigneeEl = document.createElement('div');
        if (task.assignee) {
            assigneeEl.className = 'card-assignee';
            assigneeEl.innerHTML = `<span>👤</span> <span>${escapeHTML(task.assignee)}</span>`;
        }
        metaEl.appendChild(assigneeEl);

        const tagsEl = document.createElement('div');
        tagsEl.className = 'card-tags';

        if (task.sp) {
            const spEl = document.createElement('span');
            spEl.className = 'tag tag-sp';
            spEl.textContent = `${task.sp} SP`;
            tagsEl.appendChild(spEl);
        }

        if (task.priority) {
            const prioEl = document.createElement('span');
            const p = task.priority.toLowerCase();
            prioEl.className = `tag tag-${p}`;
            prioEl.textContent = task.priority;
            tagsEl.appendChild(prioEl);
        }

        metaEl.appendChild(tagsEl);
        card.appendChild(metaEl);

        targetCol.appendChild(card);
    });
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}

function initSSE() {
    const eventSource = new EventSource('/api/stream');
    
    eventSource.onmessage = function(event) {
        // Fallback for general messages if any
    };

    eventSource.addEventListener('update', function(event) {
        const data = JSON.parse(event.data);
        
        document.getElementById('request-title').textContent = data.request_title || 'Untitled request';
        document.getElementById('current-phase').textContent = data.phase > 0 ? `Phase ${data.phase}` : 'Bootstrapping';
        document.getElementById('current-role').textContent = data.role;
        document.getElementById('current-model').textContent = data.model;
        document.getElementById('current-status').textContent = data.status;
        
        renderTimeline(data.phase);
        
        // Render Kanban if tasks are present
        if (data.tasks) {
            renderKanban(data.tasks);
        }
    });

    eventSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        document.getElementById('current-status').textContent = "Disconnected - Retrying...";
    };
}

document.addEventListener('DOMContentLoaded', () => {
    renderTimeline(0);
    initSSE();
});

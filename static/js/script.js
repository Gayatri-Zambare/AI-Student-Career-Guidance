/**
 * script.js
 * Client-side interactivity for AI-Based Student Career Guidance System.
 * Handles assessment wizard pagination, progress tracking, Chart.js graphs,
 * and AI Assistant dynamic chat.
 */

document.addEventListener("DOMContentLoaded", function () {
    initOptionStyling();
    initAssessmentWizard();
    initCharts();
    initAiAssistant();
});

// ==============================================================================
// 1. OPTION SELECTION STYLING
// ==============================================================================
function initOptionStyling() {
    const radioInputs = document.querySelectorAll('.option-label input[type="radio"]');

    radioInputs.forEach(input => {
        // Set initial selected state
        if (input.checked) {
            input.closest('.option-label').classList.add('selected');
        }

        input.addEventListener('change', function () {
            const name = this.getAttribute('name');
            // Remove 'selected' from siblings
            document.querySelectorAll(`input[name="${name}"]`).forEach(sibling => {
                sibling.closest('.option-label').classList.remove('selected');
            });
            // Add 'selected' to current
            if (this.checked) {
                this.closest('.option-label').classList.add('selected');
            }
            updateAssessmentProgress();
        });
    });
}

// ==============================================================================
// 2. ASSESSMENT WIZARD & PROGRESS TRACKING
// ==============================================================================
function initAssessmentWizard() {
    const wizardForm = document.getElementById("assessment-form");
    if (!wizardForm) return;

    const categoryPanes = document.querySelectorAll(".category-pane");
    const categoryTabs = document.querySelectorAll(".assessment-category-tab");
    const btnNext = document.getElementById("btn-next-category");
    const btnPrev = document.getElementById("btn-prev-category");
    const btnSubmit = document.getElementById("btn-submit-assessment");

    let currentCategoryIndex = 0;

    function showCategory(index) {
        categoryPanes.forEach((pane, idx) => {
            if (idx === index) {
                pane.classList.remove("d-none");
            } else {
                pane.classList.add("d-none");
            }
        });

        categoryTabs.forEach((tab, idx) => {
            if (idx === index) {
                tab.classList.add("active");
            } else {
                tab.classList.remove("active");
            }
        });

        // Toggle Prev/Next buttons
        if (btnPrev) {
            btnPrev.disabled = (index === 0);
        }
        if (btnNext) {
            if (index === categoryPanes.length - 1) {
                btnNext.classList.add("d-none");
                if (btnSubmit) btnSubmit.classList.remove("d-none");
            } else {
                btnNext.classList.remove("d-none");
                if (btnSubmit) btnSubmit.classList.add("d-none");
            }
        }

        currentCategoryIndex = index;
        window.scrollTo({ top: wizardForm.offsetTop - 80, behavior: 'smooth' });
    }

    if (categoryTabs.length > 0) {
        categoryTabs.forEach((tab, idx) => {
            tab.addEventListener("click", () => showCategory(idx));
        });
    }

    if (btnNext) {
        btnNext.addEventListener("click", () => {
            if (currentCategoryIndex < categoryPanes.length - 1) {
                showCategory(currentCategoryIndex + 1);
            }
        });
    }

    if (btnPrev) {
        btnPrev.addEventListener("click", () => {
            if (currentCategoryIndex > 0) {
                showCategory(currentCategoryIndex - 1);
            }
        });
    }

    // Submit Validation
    wizardForm.addEventListener("submit", function (e) {
        let unanswered = [];
        for (let i = 1; i <= 30; i++) {
            const checked = document.querySelector(`input[name="q${i}"]:checked`);
            if (!checked) {
                unanswered.push(i);
            }
        }

        if (unanswered.length > 0) {
            e.preventDefault();
            const firstUnansweredQ = unanswered[0];
            
            // Find which category holds this question
            const targetBlock = document.getElementById(`question-card-${firstUnansweredQ}`);
            if (targetBlock) {
                const parentPane = targetBlock.closest(".category-pane");
                categoryPanes.forEach((pane, idx) => {
                    if (pane === parentPane) {
                        showCategory(idx);
                    }
                });
                
                targetBlock.scrollIntoView({ behavior: "smooth", block: "center" });
                targetBlock.classList.add("border-danger");
                setTimeout(() => targetBlock.classList.remove("border-danger"), 3000);
            }

            alert(`Please answer all 30 assessment questions before submitting.\n\nYou have ${unanswered.length} unanswered questions (e.g., Q${firstUnansweredQ}).`);
        }
    });

    updateAssessmentProgress();
}

function updateAssessmentProgress() {
    const total = 30;
    let answered = 0;

    for (let i = 1; i <= total; i++) {
        if (document.querySelector(`input[name="q${i}"]:checked`)) {
            answered++;
        }
    }

    const progressPercent = Math.round((answered / total) * 100);
    const fillBar = document.getElementById("assessment-progress-fill");
    const countText = document.getElementById("assessment-progress-count");

    if (fillBar) fillBar.style.width = `${progressPercent}%`;
    if (countText) countText.textContent = `${answered} of ${total} Questions Answered (${progressPercent}%)`;
}

// ==============================================================================
// 3. CHART.JS VISUALIZATIONS (MONOCHROME BLACK AND WHITE THEME)
// ==============================================================================
function initCharts() {
    // 3.1 Career Compatibility Bar Chart
    const barCanvas = document.getElementById("careerBarChart");
    if (barCanvas && window.chartCareersData && window.chartScoresData) {
        new Chart(barCanvas, {
            type: 'bar',
            data: {
                labels: window.chartCareersData,
                datasets: [{
                    label: 'Compatibility Match %',
                    data: window.chartScoresData,
                    backgroundColor: [
                        '#000000',
                        '#212529',
                        '#343a40',
                        '#495057',
                        '#6c757d',
                        '#adb5bd'
                    ],
                    borderColor: '#000000',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return ` Compatibility Match: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function (val) {
                                return val + '%';
                            },
                            font: { family: 'Inter', size: 11 }
                        },
                        grid: {
                            color: '#e9ecef'
                        }
                    },
                    x: {
                        ticks: {
                            font: { family: 'Inter', size: 11, weight: '600' }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // 3.2 Skill Profile Radar Chart
    const radarCanvas = document.getElementById("skillRadarChart");
    if (radarCanvas && window.skillProfileData) {
        const labels = Object.keys(window.skillProfileData);
        const dataValues = Object.values(window.skillProfileData);

        new Chart(radarCanvas, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Demonstrated Aptitude Score',
                    data: dataValues,
                    backgroundColor: 'rgba(0, 0, 0, 0.1)',
                    borderColor: '#000000',
                    borderWidth: 2,
                    pointBackgroundColor: '#000000',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            color: '#dee2e6'
                        },
                        grid: {
                            color: '#e9ecef'
                        },
                        pointLabels: {
                            font: {
                                family: 'Inter',
                                size: 12,
                                weight: '600'
                            },
                            color: '#121212'
                        },
                        ticks: {
                            beginAtZero: true,
                            max: 100,
                            stepSize: 20,
                            display: false
                        }
                    }
                }
            }
        });
    }
}

// ==============================================================================
// 4. AI CAREER ASSISTANT (CHAT & INTERACTIVE QUERIES)
// ==============================================================================
function initAiAssistant() {
    const chatContainer = document.getElementById("ai-chat-history");
    const queryInput = document.getElementById("ai-query-input");
    const sendBtn = document.getElementById("ai-send-btn");
    const sampleChips = document.querySelectorAll(".prompt-chip");

    if (!chatContainer || !queryInput) return;

    function appendMessage(text, isUser) {
        const bubble = document.createElement("div");
        bubble.className = isUser ? "chat-bubble-user" : "chat-bubble-bot";
        bubble.innerHTML = text.replace(/\n/g, "<br>");
        chatContainer.appendChild(bubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendQuery(queryText) {
        if (!queryText.trim()) return;

        // Display user message
        appendMessage(queryText, true);
        queryInput.value = "";

        // Display typing indicator
        const typingIndicator = document.createElement("div");
        typingIndicator.className = "chat-bubble-bot";
        typingIndicator.id = "typing-placeholder";
        typingIndicator.innerHTML = "<em>Analyzing your profile and recommendations...</em>";
        chatContainer.appendChild(typingIndicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await fetch("/assistant/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query: queryText })
            });

            const data = await response.json();
            const placeholder = document.getElementById("typing-placeholder");
            if (placeholder) placeholder.remove();

            if (data.success && data.reply) {
                appendMessage(data.reply, false);
            } else {
                appendMessage("I could not generate an answer right now. Please try asking again.", false);
            }
        } catch (err) {
            const placeholder = document.getElementById("typing-placeholder");
            if (placeholder) placeholder.remove();
            appendMessage("Network or server connection error. Please try again.", false);
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", () => {
            sendQuery(queryInput.value);
        });
    }

    queryInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendQuery(queryInput.value);
        }
    });

    sampleChips.forEach(chip => {
        chip.addEventListener("click", function () {
            const prompt = this.getAttribute("data-prompt") || this.textContent.trim();
            sendQuery(prompt);
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // --- Theme Toggling ---
    const themeToggleCard = document.getElementById('theme-toggle-card');
    if (themeToggleCard) {
        const themeIcon = document.getElementById('theme-icon');
        const root = document.documentElement;

        const savedTheme = localStorage.getItem('theme') || 'light';
        root.setAttribute('data-theme', savedTheme);
        if (themeIcon) {
            themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        }

        themeToggleCard.addEventListener('click', () => {
            const currentTheme = root.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', newTheme);
            if (themeIcon) {
                themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
            }
            localStorage.setItem('theme', newTheme);
        });
    }

    // --- Rocket Simulation ---
    const timeSlider = document.querySelector('#time-slider');
    if (timeSlider) {
        const timeValue = document.querySelector('#time-value');
        const heightEl = document.querySelector('#height'); // Corrected ID from height to distance-value
        const runBtn = document.querySelector('#run-sim');
        const resetBtn = document.querySelector('#reset-sim');
        const simPanel = document.querySelector('.simulation-panel');
        let animId;

        const rocketContainer = document.createElement('div');
        rocketContainer.classList.add('rocket-container');
        Object.assign(rocketContainer.style, {
            position: 'relative',
            height: '80px',
            marginTop: '20px',
            background: '#f0f4ff',
            borderRadius: '8px',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-start'
        });

        const resultsPanelNode = document.querySelector('#sim-results');
        if (simPanel && resultsPanelNode) simPanel.insertBefore(rocketContainer, resultsPanelNode);

        const rocket = document.createElement('div');
        rocket.textContent = '🚀';
        Object.assign(rocket.style, {
            fontSize: '60px',
            position: 'absolute',
            left: '0',
            bottom: '10px'
        });
        rocketContainer.appendChild(rocket);

        function updateSliderValues() {
            timeValue.textContent = parseFloat(timeSlider.value).toFixed(1);
        }
        timeSlider.addEventListener('input', updateSliderValues);

        function animateValue(el, start, end, duration, suffix = '') {
            let startTime = null;
            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                let progress = timestamp - startTime;
                let fraction = Math.min(progress / duration, 1);
                el.textContent = (start + (end - start) * fraction).toFixed(2) + suffix;
                if (fraction < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
        }

        function runSimulation() {
            cancelAnimationFrame(animId);
            const time = parseFloat(timeSlider.value);
            const height = 5 * time * time + 3 * time + 2;
            const duration = 1500;
            animateValue(heightEl, 0, height, duration, ' meters');
            let start = null;
            const maxY = rocketContainer.offsetHeight - 40;
            function animateRocket(timestamp) {
                if (!start) start = timestamp;
                let t = (timestamp - start) / 1000;
                let fraction = Math.min(t * 0.5, 1);
                rocket.style.bottom = (fraction * maxY * (height / 500)) + 'px';
                if (fraction < 1) {
                    animId = requestAnimationFrame(animateRocket);
                }
            }
            animId = requestAnimationFrame(animateRocket);
        }

        function resetSimulation() {
            cancelAnimationFrame(animId);
            rocket.style.bottom = '10px';
            heightEl.textContent = '2.00 meters';
        }

        if (runBtn) runBtn.addEventListener('click', runSimulation);
        if (resetBtn) resetBtn.addEventListener('click', resetSimulation);
        updateSliderValues();
    }


    // --- Mode Tabs ---
    const modeButtons = document.querySelectorAll('.mode-btn');
    if (modeButtons.length > 0) {
        const basicModeDiv = document.getElementById('basic-mode');
        const advancedModeDiv = document.getElementById('advanced-mode');
        modeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                modeButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (btn.dataset.mode === 'basic') {
                    if (basicModeDiv) basicModeDiv.style.display = 'block';
                    if (advancedModeDiv) advancedModeDiv.style.display = 'none';
                } else {
                    if (basicModeDiv) basicModeDiv.style.display = 'none';
                    if (advancedModeDiv) advancedModeDiv.style.display = 'block';
                }
            });
        });
    }


    // --- Fun Facts Cycling ---
    const funFacts = document.querySelectorAll('.animated-fact');
    if (funFacts.length > 0) {
        let currentIndex = 0;
        const fadeTime = 600;
        const displayTime = 7000;

        funFacts.forEach(fact => {
            fact.style.opacity = '0';
            fact.style.transition = `opacity ${fadeTime}ms ease-in-out`;
            fact.style.display = 'none';
        });

        function cycleFacts() {
            funFacts.forEach(f => {
                f.style.opacity = '0';
                f.style.display = 'none';
            });

            const current = funFacts[currentIndex];
            current.style.display = 'block';
            setTimeout(() => current.style.opacity = '1', 50);

            setTimeout(() => {
                current.style.opacity = '0';
                setTimeout(() => {
                    current.style.display = 'none';
                    currentIndex = (currentIndex + 1) % funFacts.length;
                    cycleFacts();
                }, fadeTime);
            }, displayTime);
        }
        cycleFacts();
    }


    // --- Think & Decide Challenge ---
    const thinkButtons = document.querySelectorAll('#think-answer-buttons .btn');
    if (thinkButtons.length > 0) {
        const answerDiv = document.getElementById('think-answer');
        const correctAnswerText = 'B) The rocket\'s initial launch height';

        thinkButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                thinkButtons.forEach(b => b.disabled = true);
                const btnText = btn.textContent.trim();
                const correctLetter = correctAnswerText.charAt(0);
                const selectedLetter = btnText.charAt(0);
                if (selectedLetter === correctLetter) {
                    btn.style.background = 'linear-gradient(135deg, #00c853, #00e676)';
                    btn.style.color = 'white';
                    btn.textContent = '✔ ' + btnText;
                } else {
                    btn.style.background = 'linear-gradient(135deg, #ff3d00, #ff5722)';
                    btn.style.color = 'white';
                    btn.textContent = '✖ ' + btnText;
                    thinkButtons.forEach(b => {
                        if (b.textContent.trim().charAt(0) === correctLetter) {
                            b.style.background = 'linear-gradient(135deg, #00c853, #00e676)';
                            b.style.color = 'white';
                            b.textContent = '✔ ' + b.textContent.trim();
                        }
                    });
                }
                if(answerDiv) answerDiv.style.display = 'block';
            });
        });
    }

    // --- CodeMirror Python Editor ---
    const editorElement = document.getElementById("python-editor");
    if (editorElement) {
        const editor = CodeMirror(editorElement, {
            value: `def rocket_height(t):
    """Calculates height based on the polynomial."""
    return 5 * t**2 + 3 * t + 2

# Calculate and print for t = 0, 1, 2, 3
for time in range(4):
    height = rocket_height(time)
    print(f"At t = {time}s: Height = {height} meters")`,
            mode: "python",
            theme: "dracula",
            lineNumbers: true,
            tabSize: 4,
            indentUnit: 4,
        });

        const runBtn = document.getElementById("run-python");
        const outputBox = document.getElementById("python-output");

        if (runBtn && outputBox) {
            runBtn.addEventListener("click", async () => {
                const code = editor.getValue().trim();
                outputBox.textContent = "⏳ Running your Python code...";
                outputBox.style.color = "#00ffb0";

                try {
                    const response = await fetch("https://emkc.org/api/v2/piston/execute", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            language: "python",
                            version: "3.10.0",
                            files: [{ content: code }]
                        })
                    });
                    const data = await response.json();
                    let outputText = "";
                    if (data.run) {
                        const stdout = data.run.stdout?.trim();
                        const stderr = data.run.stderr?.trim();
                        if (stderr) {
                            outputText += "❌ Error:\n" + stderr + "\n\n";
                        }
                        if (stdout) {
                            outputText += "✅ Output:\n" + stdout;
                        }
                        if (!stdout && !stderr) {
                            outputText = "⚠️ No output or errors returned.";
                        }
                    } else {
                        outputText = "⚠️ Unexpected API response.";
                    }
                    outputBox.textContent = outputText.trim();
                    if (outputText.includes("Error") || outputText.includes("Traceback")) {
                        outputBox.style.color = "#ff6b6b";
                    } else {
                        outputBox.style.color = "#00ffb0";
                    }
                } catch (err) {
                    outputBox.textContent = "❌ Error running code: " + err.message;
                    outputBox.style.color = "#ff6b6b";
                }
            });
        }
    }

    // --- AI Reflection Feedback ---
    const reviewButton = document.getElementById('review-reflection');
    if(reviewButton) {
        const reflectionArea = document.getElementById('reflection-textarea'); // Corrected from class to ID
        const feedbackDiv = document.getElementById('ai-feedback');
        const feedbackContent = document.getElementById('ai-feedback-content');

        reviewButton.addEventListener('click', async () => {
            // IMPORTANT: API keys should NOT be stored in frontend code.
            // This is a placeholder and should be replaced by a secure backend call.
            const OPENROUTER_API_KEY = "YOUR_API_KEY_HERE";

            if (!reflectionArea || !feedbackDiv || !feedbackContent) return;
            const reflectionText = reflectionArea.value.trim();

            if (!reflectionText) {
                feedbackDiv.style.display = 'block';
                feedbackContent.textContent = 'Write or speak your thoughts first for AI review!';
                feedbackContent.style.color = '#ff6b6b';
                return;
            }

            if (OPENROUTER_API_KEY === "YOUR_API_KEY_HERE") {
                feedbackDiv.style.display = 'block';
                feedbackContent.textContent = 'AI feedback is not configured. An API key is required.';
                feedbackContent.style.color = '#ff6b6b';
                return;
            }

            feedbackDiv.style.display = 'block';
            feedbackContent.textContent = 'Analyzing...';

            try {
                const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
                        "X-Title": "Physics Reflection Tool",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        model: "deepseek/deepseek-chat-v3.1:free",
                        messages: [{
                            role: "system",
                            content: "You are a physics tutor..."
                        }, {
                            role: "user",
                            content: `Student explanation: "${reflectionText}"`
                        }],
                        max_tokens: 150
                    })
                });
                const data = await response.json();
                if (data.choices && data.choices[0]?.message?.content) {
                    feedbackContent.innerHTML = data.choices[0].message.content.trim();
                } else {
                    feedbackContent.innerHTML = '<div>⚠️ Unexpected API response format.</div>';
                }
            } catch (err) {
                feedbackContent.textContent = '❌ Error fetching feedback: ' + err.message;
            }
        });
    }

    // --- Speech-to-Text ---
    const speechButton = document.getElementById('speech-to-text');
    if (speechButton) {
        const textarea = document.getElementById('reflection-textarea');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition && textarea) {
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            let isRecognizing = false;

            speechButton.addEventListener('click', () => {
                if (isRecognizing) {
                    recognition.stop();
                } else {
                    recognition.start();
                }
            });

            recognition.onstart = () => {
                isRecognizing = true;
                speechButton.querySelector('.icon').textContent = '⏹';
                speechButton.style.background = 'linear-gradient(135deg, #ff3d00, #ff5722)';
            };

            recognition.onend = () => {
                isRecognizing = false;
                speechButton.querySelector('.icon').textContent = '🎤';
                speechButton.style.background = 'linear-gradient(135deg, #0078ff, #00d4ff)';
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                textarea.value = textarea.value ? textarea.value + ' ' + transcript : transcript;
            };

        } else {
            speechButton.disabled = true;
        }
    }
});
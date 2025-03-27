// Prompt suggestions configuration
const PROMPT_SUGGESTIONS = [
    {
        text: "Explain the code above and suggest improvements",
        icon: "fas fa-code",
        label: "Code Review"
    },
    {
        text: "Write a unit test for this function",
        icon: "fas fa-vial",
        label: "Unit Test"
    },
    {
        text: "Explain how this code works step by step",
        icon: "fas fa-list-ol",
        label: "Step-by-Step"
    },
    {
        text: "Optimize this code for better performance",
        icon: "fas fa-tachometer-alt",
        label: "Optimize"
    },
    {
        text: "Show me an example of implementing this feature",
        icon: "fas fa-lightbulb",
        label: "Example"
    },
    {
        text: "What are the best practices for this scenario?",
        icon: "fas fa-check-circle",
        label: "Best Practices"
    },
    {
        text: "Debug this code and fix potential issues",
        icon: "fas fa-bug",
        label: "Debug"
    },
    {
        text: "Compare different approaches to solve this problem",
        icon: "fas fa-balance-scale",
        label: "Compare"
    }
];

class PromptSuggestions {
    constructor() {
        this.init();
    }

    init() {
        this.createSuggestionsContainer();
        this.addScrollButtons();
    }

    createSuggestionsContainer() {
        const container = document.createElement('div');
        container.className = 'prompt-suggestions';
        container.innerHTML = `
            <div class="suggestions-scroll">
                ${PROMPT_SUGGESTIONS.map(suggestion => `
                    <button class="suggestion-chip" onclick="promptSuggestions.usePrompt('${suggestion.text}')">
                        <i class="${suggestion.icon}"></i> ${suggestion.label}
                    </button>
                `).join('')}
            </div>
        `;

        const inputContainer = document.querySelector('.input-container');
        inputContainer.insertBefore(container, inputContainer.firstChild);
    }

    usePrompt(prompt) {
        const textarea = document.getElementById('promptInput');
        textarea.value = prompt;
        textarea.focus();
        
        if (typeof autoResize === 'function') {
            autoResize(textarea);
        }
        
        textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    addScrollButtons() {
        const container = document.querySelector('.suggestions-scroll');
        const scrollAmount = 200;

        if (container.scrollWidth > container.clientWidth) {
            const scrollButtons = {
                left: this.createScrollButton('left', -1, scrollAmount),
                right: this.createScrollButton('right', 1, scrollAmount)
            };

            container.parentElement.appendChild(scrollButtons.left);
            container.parentElement.appendChild(scrollButtons.right);
        }
    }

    createScrollButton(direction, multiplier, scrollAmount) {
        const button = document.createElement('button');
        button.innerHTML = `<i class="fas fa-chevron-${direction}"></i>`;
        button.className = `scroll-button ${direction}`;
        button.onclick = () => {
            const container = document.querySelector('.suggestions-scroll');
            container.scrollBy({
                left: multiplier * scrollAmount,
                behavior: 'smooth'
            });
        };
        return button;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.promptSuggestions = new PromptSuggestions();
});
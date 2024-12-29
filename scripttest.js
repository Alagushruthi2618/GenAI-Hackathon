
const startBtn = document.querySelector('.start-btn');
const quizSection = document.querySelector('.quiz-section');
const nextBtn = document.querySelector('.next-btn');
const prevBtn = document.querySelector('.prev-btn');
const resultSection = document.querySelector('.result');
const questionText = document.querySelector('.question-text');
const optionList = document.querySelector('.option-list');
const questionTotal = document.querySelector('.question-total');
const restartBtn = document.querySelector('.restart-btn');

let questionCount = 0;
let questionNumb = 1;
let userChoices = [];

// Start the quiz when the start button is clicked
startBtn.onclick = () => {
    document.querySelector('.home').style.display = "none";
    quizSection.style.display = "block";  // Show quiz section
    showQuestions(questionCount);  // Show the first question
    questionCounter(questionNumb);
};

// Show the questions and options dynamically
function showQuestions(index) {
    questionText.textContent = `Question ${questions[index].numb}: ${questions[index].question}`;
    let options = '';

    questions[index].options.forEach((option, i) => {
        options += `<div class="option" data-option="${i}"><span>${option}</span></div>`;
    });

    optionList.innerHTML = options;

    const optionsList = document.querySelectorAll('.option');
    optionsList.forEach(option => {
        option.addEventListener('click', optionSelected);
    });
}

// Store the selected option index and highlight it
function optionSelected() {
    const selectedOptionIndex = this.getAttribute('data-option');
    userChoices[questionCount] = parseInt(selectedOptionIndex);

    const allOptions = document.querySelectorAll('.option');
    allOptions.forEach(opt => opt.classList.remove('selected'));
    this.classList.add('selected');
}

// Navigate to the next question when the "Next" button is clicked
nextBtn.onclick = () => {
    if (questionCount < questions.length - 1) {
        questionCount++;
        questionNumb++;
        showQuestions(questionCount);
        questionCounter(questionNumb);
    } else {
        showResult();  // Show result once the quiz is complete
    }
};

// Navigate to the previous question when the "Previous" button is clicked
prevBtn.onclick = () => {
    if (questionCount > 0) {
        questionCount--;
        questionNumb--;
        showQuestions(questionCount);
        questionCounter(questionNumb);
    }
};

// Update the question counter
function questionCounter(index) {
    questionTotal.textContent = `${index} of ${questions.length} Questions`;
}

// Display the result based on the user's choices
function showResult() {
    let naturalisticCount = 0;  // Count selections of option 1 (Naturalistic Intelligence)
    let spatialCount = 0;  // Count selections of any other option (Spatial Intelligence)

    // Count the selections
    userChoices.forEach(choice => {
        if (choice === 0) {
            naturalisticCount++;
        } else {
            spatialCount++;
        }
    });

    const resultText = document.querySelector('.result-text');
    if (naturalisticCount > spatialCount) {
        resultText.textContent = "You have Naturalistic Intelligence!";
    } else {
        resultText.textContent = "You have Spatial Intelligence!";
    }

    // Show the result section and hide the quiz section
    resultSection.style.display = "block";
    quizSection.style.display = "none";
}

// Restart the quiz
restartBtn.onclick = () => {
    questionCount = 0;
    questionNumb = 1;
    userChoices = [];
    resultSection.style.display = "none";
    document.querySelector('.home').style.display = "block";
};
function showResult() {
    let naturalisticCount = 0;
    let spatialCount = 0;
    
    userChoices.forEach(choice => {
        if (choice === 0) {
            naturalisticCount++;
        } else {
            spatialCount++;
        }
    });
    
    const resultText = document.querySelector('.result-text');
    const intelligenceType = naturalisticCount > spatialCount ? "Naturalistic" : "Spatial";
    const score = Math.max(naturalisticCount, spatialCount) / questions.length * 100;
    
    resultText.textContent = `You have ${intelligenceType} Intelligence!`;
    
    // Set the values in the hidden form fields
    document.getElementById('intelligence_type').value = intelligenceType;
    document.getElementById('quiz_score').value = Math.round(score);
    
    // Show the result section and hide the quiz section
    resultSection.style.display = "block";
    quizSection.style.display = "none";
}
function showResult() {
    let naturalisticCount = 0;
    let spatialCount = 0;
    
    userChoices.forEach(choice => {
        if (choice === 0) {
            naturalisticCount++;
        } else {
            spatialCount++;
        }
    });
    
    const resultText = document.querySelector('.result-text');
    const intelligenceType = naturalisticCount > spatialCount ? "Naturalistic" : "Spatial";
    const score = Math.max(naturalisticCount, spatialCount) / questions.length * 100;
    
    let description = "";
    if (intelligenceType === "Naturalistic") {
        description = `You scored ${Math.round(score)}% towards Naturalistic Intelligence! 
                      This means you have a strong connection with nature and excel at recognizing 
                      patterns in the natural world. You likely enjoy outdoor activities, 
                      studying plants or animals, and understanding environmental systems.`;
    } else {
        description = `You scored ${Math.round(score)}% towards Spatial Intelligence! 
                      This means you excel at visualizing objects and spatial dimensions. 
                      You likely have strong artistic abilities, are good at reading maps, 
                      and enjoy activities that involve design and visualization.`;
    }

    // Create a form to submit results to the database
    const formHtml = `
        <div class="result-details">
            <h2>Your Results</h2>
            <p>${description}</p>
            <form action="/save_result" method="POST">
                <input type="hidden" name="intelligence_type" value="${intelligenceType}">
                <input type="hidden" name="quiz_score" value="${Math.round(score)}">
                <button type="submit" class="save-btn">Save Results</button>
            </form>
        </div>
    `;

    resultSection.innerHTML = formHtml + `<button class="restart-btn">Restart Quiz</button>`;
    
    // Reattach event listener to the new restart button
    document.querySelector('.restart-btn').onclick = () => {
        questionCount = 0;
        questionNumb = 1;
        userChoices = [];
        resultSection.style.display = "none";
        document.querySelector('.home').style.display = "block";
    };
    
    // Show the result section and hide the quiz section
    resultSection.style.display = "block";
    quizSection.style.display = "none";
}
function showResult() {
    let naturalisticCount = 0;
    let spatialCount = 0;
    
    userChoices.forEach(choice => {
        if (choice === 0) {
            naturalisticCount++;
        } else {
            spatialCount++;
        }
    });
    
    const intelligenceType = naturalisticCount > spatialCount ? "Naturalistic" : "Spatial";
    const score = Math.max(naturalisticCount, spatialCount) / questions.length * 100;
    
    let description = "";
    if (intelligenceType === "Naturalistic") {
        description = `You scored ${Math.round(score)}% towards Naturalistic Intelligence! 
                      This means you have a strong connection with nature and excel at recognizing 
                      patterns in the natural world. You likely enjoy outdoor activities, 
                      studying plants or animals, and understanding environmental systems.`;
    } else {
        description = `You scored ${Math.round(score)}% towards Spatial Intelligence! 
                      This means you excel at visualizing objects and spatial dimensions. 
                      You likely have strong artistic abilities, are good at reading maps, 
                      and enjoy activities that involve design and visualization.`;
    }

    // Save results to sessionStorage for access in the next page
    sessionStorage.setItem('intelligence_type', intelligenceType);
    sessionStorage.setItem('quiz_score', Math.round(score));

    // Update the result section HTML
    const resultHtml = `
        <div class="result-box">
            <h2 class="result-text">Your Results</h2>
            <p>${description}</p>
            <div class="button-container">
                <a href="/dashboard" class="home-btn">Go to Home</a>
            </div>
        </div>
    `;

    resultSection.innerHTML = resultHtml;
    
    // Show the result section and hide the quiz section
    resultSection.style.display = "block";
    quizSection.style.display = "none";
}

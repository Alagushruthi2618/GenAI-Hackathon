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


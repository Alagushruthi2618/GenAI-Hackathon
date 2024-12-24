const startBtn = document.querySelector('.start-btn');
const popupInfo = document.querySelector('.popup-info');
const exitBtn = document.querySelector('.exit-btn');
const main = document.querySelector('.main');
const continueBtn = document.querySelector('.continue-btn');
const quizSection = document.querySelector('.quiz-section');
const quizBox = document.querySelector('.quiz-box');

startBtn.onclick = () => {
    popupInfo.classList.add('active');
    main.classList.add('active');
};

exitBtn.onclick = () => {
    popupInfo.classList.remove('active');
    main.classList.remove('active');
};

continueBtn.onclick = () => {
    quizSection.classList.add('active');
    popupInfo.classList.remove('active');
    main.classList.remove('active');
    quizBox.classList.add('active');
    showQuestions(0);
    questionCounter(1);
};

let questionCount = 0;
let questionNumb = 1;
const nextBtn = document.querySelector('.next-btn');
nextBtn.onclick = () => {
    if(questionCount<questions.length-1)
        {
            questionCount++;
            showQuestions(questionCount);
            questionNumb++;
            questionCounter(questionNumb);
        } 
        else{
            console.log('Questions Completed')
        }
};
const optionList =document.querySelector('.option-list');


function showQuestions(index) {
    const questionText = document.querySelector('.question-text');
    questionText.textContent = `${questions[index].numb}. ${questions[index].question}`;

    let optionTag = `
    <div class="option"><span>${questions[index].options[0]}</span></div>
    <div class="option"><span>${questions[index].options[1]}</span></div>`;
    optionList.innerHTML = optionTag;
    const option = document.querySelectorAll('.option');
    for (let i=0;i<option.length;i++){
        option[i].setAttribute('onclick','optionSelected(this)');
    }
}

function questionCounter(index) {
    const questionTotal = document.querySelector('.question-total');
    questionTotal.textContent = ` ${index} of ${questions.length}Questions`;
}
function optionSelected(option) {
    const selectedOption = option.textContent;
    
    // Save user's selection
    userChoices.push(selectedOption);
    
    // Highlight the selected option (optional)
    const options = document.querySelectorAll('.option');
    options.forEach(opt => {
        opt.classList.remove('selected');
    });
    option.classList.add('selected');
}

function showResult() {
    let naturalisticCount = 0;
    let spatialCount = 0;
    
    // Define which options lead to which intelligence type
    userChoices.forEach(choice => {
        if (choice.includes("A")) {
            naturalisticCount++;
        } else {
            spatialCount++;
        }
    });

    // Display result based on the majority choice
    const result = document.querySelector('.result');
    if (naturalisticCount > spatialCount) {
        result.textContent = "You have Naturalistic Intelligence!";
    } else {
        result.textContent = "You have Spatial Intelligence!";
    }
    result.classList.add('active');
}

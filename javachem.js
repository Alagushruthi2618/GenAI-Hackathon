const answers = {
    q1: "Helium",
    q2: "Hydrogen, Helium, Lithium, Boron",
    q3: "Hydrogen",
    q4: "Boron",
    q5: "Li",
    q6: "Beryllium",
};

document.getElementById("submit-btn").addEventListener("click", () => {
    const form = document.getElementById("test-form");
    const formData = new FormData(form);
    let score = 0;

    // Iterate over each question to check the answers
    for (const [question, correctAnswer] of Object.entries(answers)) {
        const userAnswer = formData.get(question);

        // Check if the answer is selected and correct
        if (userAnswer === correctAnswer) {
            score++;
        }
    }

    // Display the result
    const totalQuestions = Object.keys(answers).length;
    const resultDiv = document.getElementById("result");
    resultDiv.textContent = `You scored ${score} out of ${totalQuestions}!`;
    resultDiv.classList.remove("hidden");

    // Optionally, disable the form inputs after submission
    form.querySelectorAll('input').forEach(input => {
        input.disabled = true;
    });

    // Show the buttons
    document.getElementById("home-btn").classList.remove("hidden");
    document.getElementById("retake-btn").classList.remove("hidden");
    document.getElementById("save-score").classList.remove("hidden");

    // Retake the test functionality
    document.getElementById("retake-btn").addEventListener("click", () => {
        form.reset(); // Reset form to clear all answers
        form.querySelectorAll('input').forEach(input => {
            input.disabled = false; // Enable all inputs
        });
        resultDiv.classList.add("hidden"); // Hide the result
        document.getElementById("home-btn").classList.add("hidden"); // Hide the home button
        document.getElementById("retake-btn").classList.add("hidden"); // Hide the retake button
    });
});



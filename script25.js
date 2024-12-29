
// Access DOM elements
const subjectDropdown = document.getElementById("subject");
const dateContainer = document.getElementById("date-container");
const uploadContainer = document.getElementById("upload-container");
const dateInput = document.getElementById("date");
const imageUpload = document.getElementById("image-upload");
const uploadedImage = document.getElementById("uploaded-image");
const generateButton = document.getElementById("generate-button");
const learnMoreContainer = document.querySelector(".button-container"); // Container for "Learn More" button
const contentParagraph = document.querySelector(".content p"); // Paragraph to hide/show

// Create a review message below the uploaded image
const reviewMessage = document.createElement("div");
reviewMessage.textContent = "Click on the image above to review the material while we generate the comics for you. This will help you ace the test!!!";
reviewMessage.style.display = "none"; // Hidden initially
reviewMessage.style.textAlign = "center";
reviewMessage.style.color = "#555";
reviewMessage.style.fontSize = "20px";
reviewMessage.style.marginTop = "10px";
uploadContainer.appendChild(reviewMessage); // Append it to the upload container

// Create a modal for displaying the image in a larger window
const modal = document.createElement("div");
modal.style.display = "none"; // Hidden initially
modal.style.position = "fixed";
modal.style.top = "0";
modal.style.left = "0";
modal.style.width = "100%";
modal.style.height = "100%";
modal.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
modal.style.zIndex = "1000";
modal.style.justifyContent = "center";
modal.style.alignItems = "center";
document.body.appendChild(modal);

const modalImage = document.createElement("img");
modalImage.style.maxWidth = "90%";
modalImage.style.maxHeight = "90%";
modalImage.style.border = "2px solid #fff";
modal.appendChild(modalImage);

// Close modal on click
modal.addEventListener("click", function () {
  modal.style.display = "none";
});

// Initial State
dateContainer.style.display = "none";
uploadContainer.style.display = "none";
uploadedImage.style.display = "none";
generateButton.disabled = true; // Disable generate button by default
learnMoreContainer.style.display = "none"; // Hide "Learn More" button and its container
contentParagraph.style.display = "none"; // Hide the <p> element

// Show/Hide containers based on subject selection
subjectDropdown.addEventListener("change", function () {
  const subject = subjectDropdown.value;

  if (subject === "Chemistry") {
    dateContainer.style.display = "block"; // Show date container
    uploadContainer.style.display = "none"; // Hide upload container
    uploadedImage.style.display = "none"; // Hide uploaded image
    reviewMessage.style.display = "none"; // Hide review message
    generateButton.disabled = true; // Disable generate button
    learnMoreContainer.style.display = "none"; // Hide "Learn More" button
    contentParagraph.style.display = "none"; // Hide the <p> element
  } else {
    dateContainer.style.display = "none"; // Hide date container
    uploadContainer.style.display = "none"; // Hide upload container
    uploadedImage.style.display = "none"; // Hide uploaded image
    reviewMessage.style.display = "none"; // Hide review message
    generateButton.disabled = true; // Disable generate button
    learnMoreContainer.style.display = "none"; // Hide "Learn More" button
    contentParagraph.style.display = "none"; // Hide the <p> element
  }
});

// Show upload container after date is selected
dateInput.addEventListener("change", function () {
  if (dateInput.value) {
    uploadContainer.style.display = "block"; // Show upload container
    generateButton.disabled = true; // Ensure generate button remains disabled
    learnMoreContainer.style.display = "none"; // Hide "Learn More" button
    contentParagraph.style.display = "none"; // Hide the <p> element
  }
});

// Handle image upload
imageUpload.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file) {
    const validImageTypes = ["image/jpeg", "image/png", "image/gif"];

    if (validImageTypes.includes(file.type)) {
      const reader = new FileReader();

      reader.onload = function (e) {
        uploadedImage.src = e.target.result; // Set uploaded image source
        uploadedImage.style.display = "block"; // Show uploaded image
        reviewMessage.style.display = "none"; // Ensure the review message is hidden initially
        generateButton.disabled = false; // Enable generate button
        learnMoreContainer.style.display = "none"; // Hide "Learn More" button
        contentParagraph.style.display = "none"; // Hide the <p> element
      };

      reader.readAsDataURL(file); // Read file as Data URL
    } else {
      alert("Please upload a valid image file (JPEG, PNG, GIF).");
      imageUpload.value = ""; // Reset file input
      uploadedImage.style.display = "none"; // Hide uploaded image
      reviewMessage.style.display = "none"; // Hide review message
      generateButton.disabled = true; // Disable generate button
      learnMoreContainer.style.display = "none"; // Hide "Learn More" button
      contentParagraph.style.display = "none"; // Hide the <p> element
    }
  } else {
    uploadedImage.style.display = "none"; // Hide uploaded image if no file is selected
    reviewMessage.style.display = "none"; // Hide review message
    generateButton.disabled = true; // Disable generate button
    learnMoreContainer.style.display = "none"; // Hide "Learn More" button
    contentParagraph.style.display = "none"; // Hide the <p> element
  }
});

// Show modal on image click
uploadedImage.addEventListener("click", function () {
  if (uploadedImage.src) {
    modalImage.src = uploadedImage.src; // Set the modal image source
    modal.style.display = "flex"; // Show modal
  }
});

// Show review message after clicking the generate button
generateButton.addEventListener("click", function () {
  reviewMessage.style.display = "block"; // Show review message after generation
  learnMoreContainer.style.display = "block"; // Show "Learn More" button container
  contentParagraph.style.display = "block"; // Show the <p> element
});
document.addEventListener('DOMContentLoaded', function() {
  // Get the intelligence type and score from sessionStorage
  const intelligenceType = sessionStorage.getItem('intelligence_type');
  const quizScore = sessionStorage.getItem('quiz_score');
  
  // Set the values in the hidden form fields
  if (intelligenceType && quizScore) {
      document.getElementById('intelligence_type').value = intelligenceType;
      document.getElementById('quiz_score').value = quizScore;
  }
  
  // Clear the sessionStorage after setting the values
  sessionStorage.removeItem('intelligence_type');
  sessionStorage.removeItem('quiz_score');
});

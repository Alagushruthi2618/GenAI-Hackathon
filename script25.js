// Access DOM elements
const subjectSelect = document.getElementById("subject");
const dateContainer = document.getElementById("date-container");
const uploadContainer = document.getElementById("upload-container");
const dateInput = document.getElementById("date");
const imageUpload = document.getElementById("image-upload");
const uploadedImage = document.getElementById("uploaded-image");

// Show/Hide containers based on subject selection
subjectSelect.addEventListener("change", function () {
  const subject = subjectSelect.value;

  if (subject === "Chemistry") {
    dateContainer.style.display = "block"; // Show date container
    uploadContainer.style.display = "block"; // Show upload container
  } else {
    dateContainer.style.display = "none"; // Hide date container
    uploadContainer.style.display = "none"; // Hide upload container
    uploadedImage.style.display = "none"; // Hide uploaded image
  }
});

// Handle image upload
imageUpload.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file) {
    const fileType = file.type;
    const validImageTypes = ["image/jpeg", "image/png", "image/gif"];

    if (validImageTypes.includes(fileType)) {
      const reader = new FileReader();

      reader.onload = function (e) {
        uploadedImage.src = e.target.result; // Set uploaded image source
        uploadedImage.style.display = "block"; // Show uploaded image
      };

      reader.readAsDataURL(file); // Read file as Data URL
    } else {
      alert("Please upload a valid image file (JPEG, PNG, GIF).");
      imageUpload.value = ""; // Reset file input
      uploadedImage.style.display = "none"; // Hide uploaded image
    }
  } else {
    uploadedImage.style.display = "none"; // Hide uploaded image if no file is selected
  }
});

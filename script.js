

const registerButton = document.getElementById('RegisterButton');
const signInButton = document.getElementById('SignInButton');
const loginForm = document.getElementById('Login');
const registerForm = document.getElementById('Register');
const registrationForm = document.getElementById('registrationForm');
const profileImageInput = document.getElementById('profileImage');
const profilePhoto = document.getElementById('profilePhoto');

// Event listener for the "Register" link
registerButton.addEventListener('click', (event) => {
  event.preventDefault(); // Prevent default anchor behavior
  loginForm.style.display = "none";
  registerForm.style.display = "block";
});

// Event listener for the "Sign In" link
signInButton.addEventListener('click', (event) => {
  event.preventDefault(); // Prevent default anchor behavior
  loginForm.style.display = "block";
  registerForm.style.display = "none";
});

// Event listener for the registration form
registrationForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission
  const file = profileImageInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      profilePhoto.src = reader.result;
      profilePhoto.style.display = 'block';
      // Automatically switch to login form after registration
      loginForm.style.display = "block";
      registerForm.style.display = "none";
    };
    reader.readAsDataURL(file);
  } else {
    alert('Please upload a profile image!');
  }
});

document.querySelector('form[action="/login"]').addEventListener('submit', function(event) {
  const username = document.querySelector('input[name="username"]').value.trim();
  const password = document.querySelector('input[name="password"]').value.trim();
  if (!username || !password) {
      alert('Please fill in all fields.');
      event.preventDefault();
  }
});

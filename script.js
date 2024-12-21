const registerButton = document.getElementById('RegisterButton');
const signInButton = document.getElementById('SignInButton');
const loginForm = document.getElementById('Login');
const registerForm = document.getElementById('Register');

// Event listener for the "Register" link
registerButton.addEventListener('click', function (event) {
  event.preventDefault(); // Prevent default anchor behavior
  loginForm.style.display = "none";
  registerForm.style.display = "block";
});

// Event listener for the "Sign In" link
signInButton.addEventListener('click', function (event) {
  event.preventDefault(); // Prevent default anchor behavior
  loginForm.style.display = "block";
  registerForm.style.display = "none";
});

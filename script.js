const registerButton = document.getElementById('RegisterButton');
const signInButton = document.getElementById('SignInButton');
const loginForm = document.getElementById('Login');
const registerForm = document.getElementById('Register');
const profileImageInput = document.getElementById('profileImage');
const profilePhoto = document.getElementById('profilePhoto');

// Event listener for the "Register" link
registerButton.addEventListener('click', (event) => {
    event.preventDefault();
    loginForm.style.display = "none";
    registerForm.style.display = "block";
});

// Event listener for the "Sign In" link
signInButton.addEventListener('click', (event) => {
    event.preventDefault();
    loginForm.style.display = "block";
    registerForm.style.display = "none";
});

// Preview profile image
profileImageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            profilePhoto.src = e.target.result;
            profilePhoto.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

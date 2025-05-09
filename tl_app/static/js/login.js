document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("dropArea");
    const fileInput = document.getElementById("fileInput");
    const folderInput = document.getElementById("folderInput");
    const notification = document.getElementById("notification");
    const username_box = document.querySelector(".username");
    const chatIdModal = document.getElementById("chatIdModal");
    const carousel = document.getElementById("infoCarousel");
    const backgroundWrapper = document.querySelector(".background-wrapper");
    
    // Check if user has session data
    const usernameText = username_box?.querySelector("span")?.textContent;
    
    // Only show the sign-up modal if there's no username yet or it's the default
    if (usernameText && usernameText.includes("hey ") && !usernameText.includes("hey!")) {
        // User is already logged in
        if (username_box) {
            username_box.style.display = 'flex';
        }
        if (chatIdModal) {
            chatIdModal.style.display = 'none';
        }
        if (carousel) {
            carousel.style.display = 'none';
        }
        if (backgroundWrapper) {
            backgroundWrapper.classList.remove("blur");
        }
    } else {
        // Show carousel to new users
        if (carousel) {
            carousel.style.display = 'flex';
            if (backgroundWrapper) {
                backgroundWrapper.classList.add("blur");
            }
        }
        if (chatIdModal) {
            chatIdModal.style.display = 'none';
        }
        if (username_box) {
            username_box.style.display = 'none';
        }
    }

    // Initialize carousel indicators if they exist
    document.querySelectorAll(".indicator").forEach((indicator, index) => {
        indicator.addEventListener("click", () => {
            showSlide(index);
        });
    });
    
    // Add form submission event listener for direct form submission
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function(e) {
            const name = document.getElementById("nameInput").value.trim();
            const chatId = document.getElementById("chatIdInput").value.trim();
            
            if (!name || !chatId) {
                e.preventDefault(); // Stop form submission
                alert("Please enter both name and phone number.");
            } else {
                console.log("Form submitted with:", name, chatId);
                // Form will naturally submit due to action attribute
            }
        });
    }
});

let currentSlide = 0;
const slides = document.querySelectorAll(".carousel-slide");
const modal = document.getElementById("chatIdModal");
const carousel = document.getElementById("infoCarousel");
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.getElementById("nextButton");
const startBtn = document.getElementById("startButton");
const indicators = document.querySelectorAll(".indicator");
const backgroundWrapper = document.querySelector(".background-wrapper");

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.toggle("active", i === index);
    });

    indicators.forEach((indicator, i) => {
        indicator.classList.toggle("active", i === index);
    });

    prevBtn.disabled = index === 0;
    
    // Show/hide Next and Get Started buttons based on slide
    if (index === slides.length - 1) {
        nextBtn.style.display = "none";
        startBtn.style.display = "block";
    } else {
        nextBtn.style.display = "block";
        startBtn.style.display = "none";
    }
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        currentSlide++;
        showSlide(currentSlide);
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        currentSlide--;
        showSlide(currentSlide);
    }
}

function endCarousel() {
    carousel.style.display = "none";
    modal.style.display = "flex";
    backgroundWrapper.classList.remove("blur");
}

window.onload = () => {
    // Show carousel and blur background for new users
    if (!document.querySelector(".username span")?.textContent?.includes("hey ") || 
        document.querySelector(".username span")?.textContent?.includes("hey!")) {
        modal.style.display = "none"; // hide form initially
        carousel.style.display = "flex"; // show carousel
        backgroundWrapper.classList.add("blur");
         // apply blur effect
    }
    showSlide(currentSlide); // start from first slide
};
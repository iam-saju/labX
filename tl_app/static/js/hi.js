document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("dropArea");
    const fileInput = document.getElementById("fileInput");
    const folderInput = document.getElementById("folderInput");
    const notification = document.getElementById("notification");
    const username_box = document.querySelector(".username");
    const chatIdModal = document.getElementById("chatIdModal");
    
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
    } else {
        // User is not logged in
        showChatIdDialog();
        if (username_box) {
            username_box.style.display = 'none';
        }
    }

    // Add event listeners to the file drop area
    if (dropArea) {
        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => {
                dropArea.classList.add("highlight");
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => {
                dropArea.classList.remove("highlight");
            });
        });

        dropArea.addEventListener("drop", (e) => {
            const files = e.dataTransfer.files;
            fileInput.files = files;
            showNotification(files.length);
            console.log("Dropped files:", files);
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", () => {
            showNotification(fileInput.files.length);
        });
    }

    if (folderInput) {
        folderInput.addEventListener("change", () => {
            showNotification(folderInput.files.length);
        });
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

function showUploadDialog() {
    const modal = document.getElementById("uploadModal");
    modal.style.display = "flex";
}

function hideUploadDialog() {
    const modal = document.getElementById("uploadModal");
    modal.style.display = "none";
}

function showChatIdDialog() {
    const modal = document.getElementById("chatIdModal");
    if (modal) modal.style.display = "flex";
}

function hideChatIdDialog() {
    const modal = document.getElementById("chatIdModal");
    if (modal) modal.style.display = "none";
}

function submitChatId() {
    const name = document.getElementById("nameInput").value.trim();
    const chatId = document.getElementById("chatIdInput").value.trim();

    if (!name || !chatId) {
        alert("Please enter both name and phone number.");
        return;
    }

    const usernameBox = document.querySelector(".username");
    if (usernameBox) {
        const usernameText = usernameBox.querySelector("span");
        if (usernameText) {
            usernameText.textContent = "hey " + name;
            usernameBox.style.display = "flex";  // Show username once user submits
        }
    }

    // Use direct form submission instead of JS-based submission
    const form = document.getElementById("signupForm");
    if (form) {
        console.log("Submitting form with:", name, chatId);
        form.submit();
    }
    
    // Don't hide the modal until successful submission
    // The page will refresh or redirect after form submission
}

// Add these functions to your existing hi.js file

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.innerHTML = createNotificationContent(message, type);
    notification.className = `notification show ${type}`;
    
    // For non-progress notifications, auto-hide after 5 seconds
    if (type !== 'progress') {
        setTimeout(() => {
            hideNotification();
        }, 5000);
    }
    
    // Add event listener to close button
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', hideNotification);
    }
}

function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.remove('show');
}

function createNotificationContent(message, type) {
    let icon = '';
    let title = '';
    
    switch(type) {
        case 'progress':
            icon = '<span class="notification-spinner"></span>';
            title = 'Uploading';
            break;
        case 'success':
            icon = '<span class="success-icon"></span>';
            title = 'Success';
            break;
        case 'error':
            icon = '<span class="error-icon"></span>';
            title = 'Error';
            break;
        default:
            icon = '';
            title = 'Notification';
    }
    
    let content = `
        <div class="notification-header">
            <div class="notification-title">${icon}${title}</div>
            <span class="notification-close">&times;</span>
        </div>
    `;
    
    if (type === 'progress') {
        content += `
            <div class="progress-container">
                <div class="progress-bar" id="uploadProgressBar"></div>
            </div>
        `;
    }
    
    content += `<div class="notification-text">${message}</div>`;
    
    return content;
}

function updateProgressBar(percent) {
    const progressBar = document.getElementById('uploadProgressBar');
    if (progressBar) {
        progressBar.style.width = `${percent}%`;
    }
}

// File Upload with Progress
document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("dropArea");
    const fileInput = document.getElementById("fileInput");
    const folderInput = document.getElementById("folderInput");
    const notification = document.getElementById("notification");
    const username_box = document.querySelector(".username");
    const chatIdModal = document.getElementById("chatIdModal");
    const uploadForm = document.getElementById("uploadForm");
    
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
    } else {
        // User is not logged in
        showChatIdDialog();
        if (username_box) {
            username_box.style.display = 'none';
        }
    }

    // Add event listeners to the file drop area
    if (dropArea) {
        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => {
                dropArea.classList.add("highlight");
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => {
                dropArea.classList.remove("highlight");
            });
        });

        dropArea.addEventListener("drop", (e) => {
            const files = e.dataTransfer.files;
            fileInput.files = files;
            showFileCount(files.length);
            console.log("Dropped files:", files);
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", () => {
            showFileCount(fileInput.files.length);
        });
    }

    if (folderInput) {
        folderInput.addEventListener("change", () => {
            showFileCount(folderInput.files.length);
        });
    }
    
    // Handle form submission with progress tracking
    if (uploadForm) {
        uploadForm.addEventListener("submit", function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const fileCount = (fileInput.files.length || 0) + (folderInput.files.length || 0);
            
            if (fileCount === 0) {
                showNotification("Please select files to upload", "error");
                return;
            }
            
            // Show progress notification
            showNotification(`Uploading ${fileCount} files...`, "progress");
            
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener("progress", function(event) {
                if (event.lengthComputable) {
                    const percentComplete = Math.round((event.loaded / event.total) * 100);
                    updateProgressBar(percentComplete);
                }
            });
            
            xhr.addEventListener("load", function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    // Success
                    showNotification(`Successfully uploaded ${fileCount} files!`, "success");
                    setTimeout(() => {
                        hideUploadDialog();
                        // Optional: reload or redirect
                        // window.location.reload();
                    }, 1500);
                } else {
                    // Error
                    showNotification("Upload failed. Please try again.", "error");
                }
            });
            
            xhr.addEventListener("error", function() {
                showNotification("Upload failed. Please check your connection.", "error");
            });
            
            xhr.open("POST", uploadForm.action);
            xhr.send(formData);
        });
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

// Helper function to show file count notification
function showFileCount(count) {
    if (count > 0) {
        showNotification(`${count} files selected and ready to upload`, "info");
    }
}
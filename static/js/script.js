/* ==========================================================
   script.js
   ----------
   Small, dependency-free client-side behaviors:
   - Registration: live password-match check
   - Analyzer: file selection display, drag-and-drop, required-field
     validation, and a "submitting..." button state
   Nothing here talks to a server -- all real validation and processing
   happens in Flask (Member 1) and the ML/parser modules (Members 2 & 3).
   ========================================================== */

document.addEventListener("DOMContentLoaded", function () {
    initRegisterForm();
    initAnalyzerForm();
});

/* ---------------- Register page: password match ---------------- */
function initRegisterForm() {
    const form = document.getElementById("registerForm");
    if (!form) return;

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");
    const mismatchWarning = document.getElementById("passwordMismatch");

    function checkMatch() {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            mismatchWarning.style.display = "block";
        } else {
            mismatchWarning.style.display = "none";
        }
    }

    password.addEventListener("input", checkMatch);
    confirmPassword.addEventListener("input", checkMatch);

    form.addEventListener("submit", function (e) {
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            mismatchWarning.style.display = "block";
        }
    });
}

/* ---------------- Analyzer page: upload + validation ---------------- */
function initAnalyzerForm() {
    const form = document.getElementById("analyzeForm");
    if (!form) return;

    const fileInput = document.getElementById("resumeInput");
    const dropZone = document.getElementById("uploadDrop");
    const fileNameLabel = document.getElementById("fileName");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const analyzeBtnText = document.getElementById("analyzeBtnText");

    function showFileName() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameLabel.textContent = file.name;
        } else {
            fileNameLabel.textContent = "";
        }
    }

    fileInput.addEventListener("change", showFileName);

    // Drag-and-drop support on the drop zone
    ["dragover", "dragenter"].forEach(function (eventName) {
        dropZone.addEventListener(eventName, function (e) {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(function (eventName) {
        dropZone.addEventListener(eventName, function (e) {
            e.preventDefault();
            dropZone.classList.remove("dragover");
        });
    });

    dropZone.addEventListener("drop", function (e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            showFileName();
        }
    });

    form.addEventListener("submit", function (e) {
        const jobDescription = document.getElementById("jobDescription");

        if (fileInput.files.length === 0) {
            e.preventDefault();
            alert("Please choose a resume PDF before analyzing.");
            return;
        }

        const fileName = fileInput.files[0].name.toLowerCase();
        if (!fileName.endsWith(".pdf")) {
            e.preventDefault();
            alert("Only PDF files are supported.");
            return;
        }

        if (!jobDescription.value.trim()) {
            e.preventDefault();
            alert("Please paste a job description.");
            return;
        }

        // Give the user feedback that analysis is running (parsing +
        // TF-IDF can take a moment on the server).
        analyzeBtn.disabled = true;
        analyzeBtnText.textContent = "Analyzing...";
    });
}

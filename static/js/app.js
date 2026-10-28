let currentRelPath = ".";
let selectedFiles = new Set();
let passwordRequired = false;
let serverPassword = null;

const authSection = document.getElementById("auth-section");
const mainContent = document.getElementById("main-content");
const passwordInput = document.getElementById("password-input");
const loginButton = document.getElementById("login-button");
const authError = document.getElementById("auth-error");
const fileList = document.getElementById("file-list");
const currentPathSpan = document.getElementById("current-path");
const backButton = document.getElementById("back-button");
const downloadButton = document.getElementById("download-button");
const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-button");
const progressContainer = document.getElementById("progress-container");
const progressBar = document.getElementById("progress-bar");
const uploadStatus = document.getElementById("upload-status");

async function checkAuth() {
    const response = await fetch("/list");
    if (response.status === 401 || response.status === 403) {
        passwordRequired = true;
        authSection.classList.remove("hidden");
    } else if (response.status === 200) {
        showMainContent();
    } else {
        authSection.classList.remove("hidden");
    }
}

async function showMainContent() {
    authSection.classList.add("hidden");
    mainContent.classList.remove("hidden");
    await loadFiles();
}

async function loadFiles() {
    const response = await fetch(`/list?rel_path=${encodeURIComponent(currentRelPath)}`);
    if (response.ok) {
        const data = await response.json();
        renderFiles(data.entries);
        currentPathSpan.textContent = currentRelPath;
    } else {
        console.error("Failed to load files");
    }
}

function renderFiles(entries) {
    fileList.innerHTML = "";
    entries.forEach(entry => {
        const li = document.createElement("li");
        const icon = entry.is_dir ? "📁" : "📄";
        li.innerHTML = `<span>${icon} ${entry.name}</span>`;
        
        if (entry.is_dir) {
            li.onclick = () => {
                currentRelPath = currentRelPath === "." ? entry.name : `${currentRelPath}/${entry.name}`;
                loadFiles();
            };
        } else {
            li.onclick = () => {
                if (selectedFiles.has(entry.name)) {
                    selectedFiles.delete(entry.name);
                    li.classList.remove("selected");
                } else {
                    selectedFiles.add(entry.name);
                    li.classList.add("selected");
                }
                downloadButton.disabled = selectedFiles.size === 0;
            };
        }
        fileList.appendChild(li);
    });

    if (currentRelPath !== ".") {
        const li = document.createElement("li");
        li.innerHTML = `<span>⤴️ ..</span>`;
        li.onclick = () => {
            const parts = currentRelPath.split("/");
            parts.pop();
            currentRelPath = parts.length === 1 ? "." : parts.join("/");
            loadFiles();
        };
        fileList.prepend(li);
    }
}

loginButton.onclick = async () => {
    const password = passwordInput.value;
    const formData = new FormData();
    formData.append("password", password);
    
    const response = await fetch("/auth", {
        method: "POST",
        body: formData
    });
    
    if (response.ok) {
        showMainContent();
    } else {
        authError.classList.remove("hidden");
    }
};

backButton.onclick = () => {
    const parts = currentRelPath.split("/");
    if (parts.length > 1) {
        parts.pop();
        currentRelPath = parts.length === 1 ? "." : parts.join("/");
        loadFiles();
    } else {
        currentRelPath = ".";
        loadFiles();
    }
};

uploadButton.onclick = async () => {
    const files = fileInput.files;
    if (files.length === 0) return;

    progressContainer.classList.remove("hidden");
    uploadStatus.textContent = "Uploading...";
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";

    const formData = new FormData();
    formData.append("rel_path", currentRelPath);
    for (const file of files) {
        formData.append("files", file);
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    
    xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
            const percent = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percent + "%";
            progressBar.textContent = percent + "%";
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            uploadStatus.textContent = "Upload completed!";
            progressBar.style.width = "0%";
            progressBar.textContent = "";
            setTimeout(() => {
                progressContainer.classList.add("hidden");
                uploadStatus.textContent = "";
            }, 3000);
            loadFiles();
        } else {
            uploadStatus.textContent = "Upload failed.";
        }
    };

    xhr.send(formData);
};

downloadButton.onclick = async () => {
    const formData = new FormData();
    for (const name of selectedFiles) {
        formData.append("file_names", name);
    }
    formData.append("rel_path", currentRelPath);

    const response = await fetch("/download", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "download.zip";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        selectedFiles.clear();
        loadFiles();
    } else {
        alert("Download failed");
    }
};

checkAuth();

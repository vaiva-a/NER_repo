function openAddUserDialog() {
    document.getElementById("addUserDialog").style.display = "block";
}

function closeAddUserDialog() {
    document.getElementById("addUserDialog").style.display = "none";
    document.getElementById("addUserForm").reset();
}

function submitNewUser(event) {
    event.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    fetch("/add_annotator/", {
        method: "POST",
        body: JSON.stringify({
            username: username,
            password: password,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                alert("User added successfully!");
                closeAddUserDialog();
            } else {
                alert(data.message || "Error adding user!");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Failed to add user.");
        });
}
function showAddTagDialog() {
    const dialog = document.getElementById("addTagDialog");
    dialog.style.display = "flex"; // Show the dialog
}
function closeAddTagDialog() {
    const dialog = document.getElementById("addTagDialog");
    dialog.style.display = "none"; // Hide the dialog
}
function submitNewTag() {
    const newTag = document.getElementById("newTagInput").value.trim();
    if (newTag) {
        fetch("/add_tag/", {
            method: "POST",
            body: JSON.stringify({ tag: newTag }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    alert("Tag added!");
                    // Clear the input and close the dialog
                    let a = document.getElementById("newTagInput").value;
                    document.getElementById("newTagInput").value = "";

                    // Create new tag element
                    let newTag = document.createElement("div");
                    newTag.classList.add("tag");
                    // newTag.setAttribute('onclick', `selectTag('${newTagInput}')`);
                    console.log(a);
                    newTag.innerHTML = `
                  <span onclick="selectTag('${a}')">${a}</span>
                  <span class="delete-tag" onclick="confirmDeleteTag('${a}')">🗑️</span>
              `;
                    let topTagsDiv = document.getElementById("tagSelector");
                    topTagsDiv.appendChild(newTag);
                    closeAddTagDialog();
                } else {
                    alert("Error adding tag! Tag might already exist!");
                    document.getElementById("newTagInput").value = "";
                    closeAddTagDialog();
                }
            })
            .catch((error) => {
                console.error("Error adding tag:", error);
                alert("Failed to add tag.");
            });
    } else {
        alert("Tag name cannot be empty!");
    }
}
function clearTags() {
    fetch("/clear_tags/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status == "success") {
                // Clear the tag-list div
                // const tagListDiv = document.querySelector('.tag-list');
                // tagListDiv.innerHTML = ''; // Remove all tags from the UI
                alert(data.message);
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch((error) => {
            console.error("Error clearing tags:", error);
            alert("Failed to clear tags.");
        });
}
document
    .getElementById("file-input")
    .addEventListener("change", handleFileUpload);

function handleFileUpload(event) {
    //event.preventDefault();
    const file = event.target.files
        ? event.target.files[0]
        : event.dataTransfer.files[0];

    if (!file) {
        alert("No file selected!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload_file/", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json()) // Ensure JSON parsing
        .then((data) => {
            if (data.status === "success") {
                alert("File uploaded successfully!");
            } else {
                alert("File upload failed: " + data.message);
            }
        })
        .catch((error) => {
            console.error("Upload Error:", error);
            alert("File upload failed.");
        });
}
document.addEventListener("DOMContentLoaded", fetchResultFiles);

function fetchResultFiles() {
    fetch("/list_results/")
        .then((response) => response.json())
        .then((data) => {
            const resultList = document.getElementById("result-files-list");
            resultList.innerHTML = ""; // Clear existing list

            data.files.forEach((file) => {
                const listItem = document.createElement("li");
                listItem.textContent = file;

                const downloadButton = document.createElement("button");
                downloadButton.textContent = "Download \u21E9";
                downloadButton.onclick = () => downloadFile(file);

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete 🗑️";
                deleteButton.classList.add("delete-btn");
                deleteButton.onclick = () => deleteFile(file);

                listItem.appendChild(downloadButton);
                listItem.appendChild(deleteButton);

                resultList.appendChild(listItem);
            });
        })
        .catch((error) => console.error("Error fetching files:", error));
}
document.addEventListener("DOMContentLoaded", fetchUploadedFiles);
function fetchUploadedFiles() {
    fetch("/list_uploads/")
        .then((response) => response.json())
        .then((data) => {
            const resultList = document.getElementById("upload-files-list");
            resultList.innerHTML = ""; // Clear existing list

            data.files.forEach((file) => {
                const listItem = document.createElement("li");
                listItem.textContent = file;

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete 🗑️";
                deleteButton.classList.add("delete-btn");
                deleteButton.onclick = () => deleteUploadFile(file);

                listItem.appendChild(deleteButton);

                resultList.appendChild(listItem);
            });
        })
        .catch((error) => console.error("Error fetching files:", error));
}


function downloadFile(filename) {
    window.location.href = `/download_result/?filename=${encodeURIComponent(
        filename
    )}`;
}

function deleteFile(filename) {
    if (confirm(`Are you sure you want to delete ${filename}?`)) {
        fetch("/delete_result/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ filename: filename }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    alert("File deleted successfully!");
                    fetchResultFiles(); // Refresh the file list
                } else {
                    alert("Error deleting file!");
                }
            })
            .catch((error) => {
                console.error("Error deleting file:", error);
                alert("Failed to delete file.");
            });
    }
}
function deleteUploadFile(filename) {
    if (confirm(`Are you sure you want to delete ${filename}?`)) {
        fetch("/delete_upload/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ filename: filename }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    alert("File deleted successfully!");
                    fetchResultFiles(); // Refresh the file list
                } else {
                    alert("Error deleting file!");
                }
            })
            .catch((error) => {
                console.error("Error deleting file:", error);
                alert("Failed to delete file.");
            });
    }
}


// function handleFileUpload(file) {
//     const formData = new FormData();
//     formData.append("file", file);

//     fetch("/upload_file/", {
//         method: "POST",
//         body: formData
//     })
//         .then(response => response.json())
//         .then(data => {
//             alert(data.message);
//         })
//         .catch(error => {
//             console.error("File upload failed:", error);
//             alert("Error uploading file.");
//         });
// }

function triggerFileInput() {
    document.getElementById("file-input").click();
}

document
    .getElementById("file-input")
    .addEventListener("change", function (event) {
        if (event.target.files.length > 0) {
            handleFileUpload(event.target.files[0]);
        }
    });

function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
}

function handleDrop(event) {
    event.preventDefault();
    handleFileUpload(event);
}
function confirmDeleteTag(tagName) {
    if (confirm(`Are you sure you want to delete the tag "${tagName}"?`)) {
        deleteTag(tagName);
    }
}

function deleteTag(tagName) {
    fetch("/delete_tag/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCsrfToken(),
        },
        body: new URLSearchParams({ tag: tagName }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                alert(data.message);
                // Remove the tag from the DOM without reloading the page
                const tagElements =
                    document.querySelectorAll("#tagSelector .tag");
                tagElements.forEach((tagElement) => {
                    if (tagElement.innerText.trim().includes(tagName)) {
                        tagElement.remove();
                    }
                });
            } else {
                alert(data.message);
            }
        })
        .catch((error) => console.error("Error:", error));
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue;
}
function addTag() {
    const tagInput = document.getElementById("tagInput").value;
    console.log("new check");

    fetch("/add_tag/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCsrfToken(),
        },
        body: `tag=${encodeURIComponent(tagInput)}`,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                // Clear input

                console.log("checkking", newTag);
            } else {
                alert(data.message);
            }
        })
        .catch((error) => console.error("Error:", error));
}
function filterTags() {
    let searchInput = document.getElementById("tagSearch").value.toLowerCase();
    let tags = document.querySelectorAll("#tagSelector .tag");

    tags.forEach(tag => {
        let tagName = tag.querySelector("span").textContent.toLowerCase();
        if (tagName.startsWith(searchInput)) {
            tag.style.display = "flex"; // Show matching tags
        } else {
            tag.style.display = "none"; // Hide non-matching tags
        }
    });
}

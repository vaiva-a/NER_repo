


// function showAddTagDialog() {
//     const dialog = document.getElementById("addTagDialog");
//     dialog.style.display = "flex"; // Show the dialog
// }
// function closeAddTagDialog() {
//     const dialog = document.getElementById("addTagDialog");
//     dialog.style.display = "none"; // Hide the dialog
// }
// function submitNewTag() {
//     const newTag = document.getElementById("newTagInput").value.trim();
//     if (newTag) {
//         fetch("/add_tag/", {
//             method: "POST",
//             body: JSON.stringify({ tag: newTag }),
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })
//             .then((response) => response.json())
//             .then((data) => {
//                 if (data.status === "success") {
//                     alert("Tag added!");
//                     // Clear the input and close the dialog
//                     let a = document.getElementById("newTagInput").value;
//                     document.getElementById("newTagInput").value = "";

//                     // Create new tag element
//                     let newTag = document.createElement("div");
//                     newTag.classList.add("tag");
//                     // newTag.setAttribute('onclick', `selectTag('${newTagInput}')`);
//                     console.log(a);
//                     newTag.innerHTML = `
//                   <span onclick="selectTag('${a}')">${a}</span>
//                   <span class="delete-tag" onclick="confirmDeleteTag('${a}')">
//                     <img src="{% static 'images/delete-icon.png' %}" alt="Icon" width="20" height="20">
//                   </span>
//               `;
//                     let topTagsDiv = document.getElementById("tagSelector");
//                     topTagsDiv.appendChild(newTag);
//                     closeAddTagDialog();
//                 } else {
//                     alert("Error adding tag! Tag might already exist!");
//                     document.getElementById("newTagInput").value = "";
//                     closeAddTagDialog();
//                 }
//             })
//             .catch((error) => {
//                 console.error("Error adding tag:", error);
//                 alert("Failed to add tag.");
//             });
//     } else {
//         alert("Tag name cannot be empty!");
//     }
// }

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

                // Create Download Button
                const downloadButton = document.createElement("button");
                downloadButton.onclick = () => downloadFile(file);
                // Append icon and text inside button

                downloadButton.appendChild(document.createTextNode(" Download "));

                // Create Image Element for Icon
                const downloadIcon = document.createElement("img");
                downloadIcon.src = "/static/images/download-icon.png";  // Update with your actual image path
                downloadIcon.alt = "Download";
                downloadIcon.width = 20; // Adjust size as needed
                downloadIcon.height = 20;
                downloadButton.appendChild(downloadIcon);


                // Create Delete Button
                const deleteButton = document.createElement("button");
                deleteButton.classList.add("delete-btn");
                deleteButton.onclick = () => deleteFile(file);

                deleteButton.appendChild(document.createTextNode(" Delete "));

                // Create Image Element for Delete Icon
                const deleteIcon = document.createElement("img");
                deleteIcon.src = "/static/images/delete-icon.png";  // Update with your actual image path
                deleteIcon.alt = "Delete";
                deleteIcon.width = 20;
                deleteIcon.height = 20;

                // Append icon and text inside button
                deleteButton.appendChild(deleteIcon);


                // Append buttons to list item
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
                deleteButton.textContent = "Delete ";
                deleteButton.classList.add("delete-btn");
                const deleteIcon = document.createElement("img");
                deleteIcon.src = "/static/images/delete-icon.png";
                deleteIcon.alt = "Delete";
                deleteIcon.width = 20;
                deleteIcon.height = 20;
                deleteButton.appendChild(deleteIcon);
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




function getCsrfToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue;
}
// function addTag() {
//     const tagInput = document.getElementById("tagInput").value;
//     console.log("new check");

//     fetch("/add_tag/", {list
//         method: "POST",
//         headers: {
//             "Content-Type": "application/x-www-form-urlencoded",
//             "X-CSRFToken": getCsrfToken(),
//         },
//         body: `tag=${encodeURIComponent(tagInput)}`,
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             if (data.status === "success") {
//                 // Clear input

//                 console.log("checkking", newTag);
//             } else {
//                 alert(data.message);
//             }
//         })
//         .catch((error) => console.error("Error:", error));
// }


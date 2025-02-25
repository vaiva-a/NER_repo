let lines = [];
let fileName = "";
let allTagData = [];
let tagUsageCount = {}; // Store tag usage counts

let tagShortcuts = {};
const tags = JSON.parse(tag1.replace(/'/g, '"'));
console.log(tags);

document.addEventListener("DOMContentLoaded", () => {
  fetch("/get_paragraph/")
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        lines = data.paragraph.split(".");
        fileName = data.filename;
        displayAllLines();
        document.getElementById("currentFileName").innerText = data.filename;
      }
    });
  populateTagList();
});

document.addEventListener("keydown", (event) => {
  if (event.ctrlKey && event.key === "a") {
    event.preventDefault();
    assignTag();
  }
});

function populateTagList() {
  let tagListDiv = document.getElementById("tagList");
  tagListDiv.innerHTML = "";

  tags.forEach((tag) => {
    let tagDiv = document.createElement("div");
    console.log(tag);
    tagDiv.innerText = tag;
    tagDiv.value = tag;
    tagDiv.onclick = () => selectTag(tag);
    tagListDiv.appendChild(tagDiv);
  });
}

function filterTags() {
  let query = document.getElementById("tagSearch").value.toLowerCase();
  let tagListDiv = document.getElementById("tagList");
  let tagItems = tagListDiv.children;
  for (let item of tagItems) {
    item.style.display = item.innerText.toLowerCase().includes(query)
      ? "block"
      : "none";
  }
}

function selectTag(tag) {
  document.getElementById("tagSearch").value = tag;
}

function displayAllLines() {
  let sentencesContainer = document.getElementById("sentencesContainer");
  sentencesContainer.innerHTML = "";

  lines.forEach((line, index) => {
    let words = line.trim().split(" ");
    let tagData = {};
    let sentenceDiv = document.createElement("div");
    sentenceDiv.className = "mb-4 p-2 border rounded bg-gray-100";
    sentenceDiv.dataset.index = index;

    words.forEach((word, idx) => {
      let cleanWord = word.replace(/[^a-zA-Z0-9]/g, "");
      if (cleanWord) {
        tagData[idx] = { word: cleanWord, tag: "O" };
        let wordDiv = document.createElement("div");
        wordDiv.className = "word";
        wordDiv.innerText = word;
        wordDiv.onclick = () => selectWord(wordDiv, index, idx);
        sentenceDiv.appendChild(wordDiv);
      }
    });

    allTagData[index] = { sentence_number: index, annotations: tagData };
    sentencesContainer.appendChild(sentenceDiv);
  });
}

function selectWord(wordDiv, sentenceIndex, wordIndex) {
  document
    .querySelectorAll(".word")
    .forEach((w) => w.classList.remove("selected"));
  wordDiv.classList.add("selected");
  wordDiv.dataset.sentenceIndex = sentenceIndex;
  wordDiv.dataset.wordIndex = wordIndex;
}

// function assignTag() {
//   let selectedWordDiv = document.querySelector(".word.selected");
//   if (!selectedWordDiv) {
//     alert("Select a word first!");
//     return;
//   }
//   let selectedTag = document.getElementById("tagSearch").value;
//   if (!tags.includes(selectedTag)) {
//     alert("Invalid tag!");
//     return;
//   }
//   let sentenceIndex = selectedWordDiv.dataset.sentenceIndex;
//   let wordIndex = selectedWordDiv.dataset.wordIndex;
//   allTagData[sentenceIndex].annotations[wordIndex].tag = selectedTag;

//   const tagColors = {
//     person: "blue",
//     location: "green",
//     object: "orange",
//     building: "brown",
//     None: "#edf2f7",
//   };

//   selectedWordDiv.style.backgroundColor = tagColors[selectedTag] || "lightblue";
//   selectedWordDiv.style.color = selectedTag === "None" ? "#2d3748" : "white";

//   tagUsageCount[selectedTag] = (tagUsageCount[selectedTag] || 0) + 1;
//   updateTopTags();
// }
function assignTag() {
  let selectedWordDiv = document.querySelector(".word.selected");
  if (!selectedWordDiv) {
    showNotification("Please select a word first", "error");
    return;
  }

  let selectedTag = document.getElementById("tagSearch").value;
  if (!tags.includes(selectedTag)) {
    showNotification("Invalid tag selected", "error");
    return;
  }

  let sentenceIndex = selectedWordDiv.dataset.sentenceIndex;
  let wordIndex = selectedWordDiv.dataset.wordIndex;

  // Prevent redundant updates
  if (
    allTagData[sentenceIndex] &&
    allTagData[sentenceIndex].annotations[wordIndex].tag === selectedTag
  ) {
    showNotification("Word is already tagged with this entity", "info");
    return;
  }

  if (allTagData[sentenceIndex]) {
    allTagData[sentenceIndex].annotations[wordIndex].tag = selectedTag;
  }

  // Remove all previous tag classes before adding new one
  selectedWordDiv.classList.forEach((cls) => {
    if (cls.startsWith("tag-")) {
      selectedWordDiv.classList.remove(cls);
    }
  });

  selectedWordDiv.classList.add(`tag-${selectedTag.toLowerCase()}`);

  // Remove existing tag label if any
  let existingTagLabel = selectedWordDiv.querySelector(".tag-label");
  if (existingTagLabel) {
    existingTagLabel.remove();
  }

  // Create and append tag label
  let tagLabel = document.createElement("div");
  tagLabel.className = "tag-label";
  tagLabel.innerText = selectedTag;
  selectedWordDiv.appendChild(tagLabel);

  // Update tag usage count only if it's a new tag assignment
  if (!selectedWordDiv.dataset.tagged) {
    tagUsageCount[selectedTag] = (tagUsageCount[selectedTag] || 0) + 1;
    updateTopTags();
    selectedWordDiv.dataset.tagged = "true"; // Mark as tagged to prevent multiple increments
  }

  // Show success notification
  showNotification(
    `Tagged "${selectedWordDiv.innerText}" as ${selectedTag}`,
    "success"
  );

  // Auto-select next word if available
  selectNextWord(selectedWordDiv);
}


// Helper function to show notifications
// Store active notifications to prevent duplicates
let activeNotifications = new Set();

function showNotification(message, type) {
  // Check if notification container exists, if not create it
  let notifContainer = document.getElementById("notification-container");
  if (!notifContainer) {
    notifContainer = document.createElement("div");
    notifContainer.id = "notification-container";
    notifContainer.style.position = "fixed";
    notifContainer.style.bottom = "20px";
    notifContainer.style.right = "20px";
    notifContainer.style.zIndex = "1000";
    document.body.appendChild(notifContainer);
  }

  // Avoid showing the same notification multiple times
  if (activeNotifications.has(message)) {
    return;
  }
  activeNotifications.add(message);

  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.innerText = message;
  notification.style.padding = "12px 16px";
  notification.style.marginBottom = "10px";
  notification.style.borderRadius = "6px";
  notification.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
  notification.style.animation = "fadeIn 0.3s, fadeOut 0.3s 2.7s";
  notification.style.fontWeight = "500";

  if (type === "success") {
    notification.style.backgroundColor = "#48bb78";
    notification.style.color = "white";
  } else if (type === "error") {
    notification.style.backgroundColor = "#f56565";
    notification.style.color = "white";
  }

  notifContainer.appendChild(notification);

  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.remove();
    activeNotifications.delete(message); // Allow future notifications for new actions
  }, 3000);
}

// Function to automatically select the next word
function selectNextWord(currentWordDiv) {
  const words = Array.from(document.querySelectorAll(".word"));
  const currentIndex = words.indexOf(currentWordDiv);

  if (currentIndex < words.length - 1) {
    currentWordDiv.classList.remove("selected");
    if (words[currentIndex + 1]) {
      words[currentIndex + 1].classList.add("selected");
      words[currentIndex + 1].scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  }
}

// Improved function to update top tags display
function updateTopTags() {
  const topTagsList = document.getElementById("topTagsList");
  topTagsList.innerHTML = "";

  // Get tags sorted by usage count
  const sortedTags = Object.entries(tagUsageCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  const tagColors = {
    person: "#4299e1",
    location: "#48bb78",
    object: "#ed8936",
    building: "#a0522d",
    None: "#edf2f7",
  };
  let index = 0;
  sortedTags.forEach(([tag, count]) => {
    const tagItem = document.createElement("div");
    tagItem.className = "top-tag-item";
    tagShortcuts[index + 1] = tag;
    index++;
    console.log(tag);

    console.log("here", tagShortcuts);
    const tagName = document.createElement("span");
    tagName.className = "top-tag-name";
    tagName.innerText = tag;
    tagName.style.backgroundColor = tagColors[tag.toLowerCase()] || "#718096";
    tagName.style.color = tag.toLowerCase() === "none" ? "#2d3748" : "white";

    const tagCount = document.createElement("span");
    tagCount.className = "top-tag-count";
    tagCount.innerText = count;

    tagItem.appendChild(tagName);
    tagItem.appendChild(tagCount);
    topTagsList.appendChild(tagItem);
  });
  updateShortcuts();
}
function updateShortcuts() {
  const topTags = document.querySelectorAll("#topTagsList .top-tag-item");
  const shortcutsContainer = document.getElementById("shortcutsDisplay");
  
  shortcutsContainer.innerHTML = ""; // Clear existing shortcuts

  topTags.forEach((tag, index) => {
      if (index < 5) { // Only take the top 5 tags
          const tagName = tag.querySelector(".top-tag-name").innerText;
          const shortcutNumber = index + 1; // Assign shortcut (1-5)
          
          const shortcutElement = document.createElement("div");
          shortcutElement.classList.add("shortcut-item");

          shortcutElement.innerHTML = `
              <span class="shortcut-tag">${tagName}</span>
              <span class="shortcut-key">${shortcutNumber}</span>
          `;

          shortcutsContainer.appendChild(shortcutElement);
      }
  });
}

// Call this function after updating the top tags


document.addEventListener("keydown", function (event) {
  let num = event.key;
  if (num >= "1" && num <= "5" && tagShortcuts[num]) {
    document.getElementById("tagSearch").value = tagShortcuts[num];
    assignTag();
  }
  console.log(tagShortcuts[num]);
});

function submitFile() {
  let formattedTagData = allTagData.map((sentenceData) => {
    let annotations = {};
    Object.values(sentenceData.annotations).forEach(({ word, tag }) => {
      annotations[word] = tag;
    });
    return { sentence_number: sentenceData.sentence_number, annotations };
  });

  let payload = {
    filename: fileName,
    data: formattedTagData,
  };
  fetch("/submit_file/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      location.reload();
    });
}

function skipFile() {
  const currentFileName = document.getElementById("currentFileName").innerText;

  fetch(`/skip_file/?currentFileName=${encodeURIComponent(currentFileName)}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        // Update the lines array and current file
        lines = data.paragraph.split(".");
        fileName = data.filename;
        displayAllLines();
        document.getElementById("currentFileName").innerText = data.filename;
      } else {
        alert("no more files");
      }
    })
    .catch((error) => {
      console.error("Error skipping file:", error);
      document.getElementById("paraContent").innerText = "Failed to skip file.";
    });
}

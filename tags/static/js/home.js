let lines = [];
let fileName = "";
let allTagData = [];
let tagUsageCount = {}; // Store tag usage counts
let autotaglist = {};
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
        console.log("here", data.taglist);
        autotaglist = data.taglist;
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

        let tagDiv = document.createElement("div");
        tagDiv.className = "tag";
        tagDiv.innerText = "O";
        wordDiv.appendChild(tagDiv); // Append tag inside word

        sentenceDiv.appendChild(wordDiv);
      }
    });

    allTagData[index] = { sentence_number: index, annotations: tagData };
    sentencesContainer.appendChild(sentenceDiv);
  });
}

function AutoTag() {
  console.log("here")
  let sentencesContainer = document.getElementById("sentencesContainer");
  sentencesContainer.innerHTML = ""; // Clear previous content

  Object.keys(autotaglist).forEach((sentenceIndex) => {
    let sentenceData = autotaglist[sentenceIndex];
    let sentenceDiv = document.createElement("div");
    sentenceDiv.className = "mb-4 p-2 border rounded bg-gray-100";
    sentenceDiv.dataset.index = sentenceIndex;

    let tagData = {};

    Object.keys(sentenceData.annotations).forEach((wordIndex) => {
      let wordInfo = sentenceData.annotations[wordIndex];
      let word = wordInfo.word;
      let tag = wordInfo.tag || "O";

      let wordDiv = document.createElement("div");
      wordDiv.className = "word";
      wordDiv.innerText = word;
      wordDiv.onclick = () => selectWord(wordDiv, sentenceIndex, wordIndex);

      let tagDiv = document.createElement("div");
      tagDiv.className = "tag";
      tagDiv.innerText = tag;
      wordDiv.appendChild(tagDiv); // Append tag inside word div

      sentenceDiv.appendChild(wordDiv);

      tagData[wordIndex] = { word, tag };
    });

    allTagData[sentenceIndex] = { sentence_number: sentenceIndex, annotations: tagData };
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
  if(allTagData[sentenceIndex]){
    allTagData[sentenceIndex].annotations[wordIndex].tag = selectedTag;
  }
  

  // Remove all tag classes first
  selectedWordDiv.classList.remove("tag-person", "tag-location", "tag-object", "tag-building", "tag-none");
  
  // Add the appropriate tag class
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

  // Update tag usage statistics
  tagUsageCount[selectedTag] = (tagUsageCount[selectedTag] || 0) + 1;
  updateTopTags();
  
  // Show success notification
  showNotification(`Tagged "${selectedWordDiv.innerText}" as ${selectedTag}`, "success");
  
  // Auto-select next word if available
  selectNextWord(selectedWordDiv);
}

// Helper function to show notifications
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
  }, 3000);
}

// Function to automatically select the next word
function selectNextWord(currentWordDiv) {
  const words = Array.from(document.querySelectorAll(".word"));
  const currentIndex = words.indexOf(currentWordDiv);
  
  if (currentIndex < words.length - 1) {
    currentWordDiv.classList.remove("selected");
    if(words[currentIndex + 1]){
      words[currentIndex + 1].classList.add("selected");
      words[currentIndex + 1].scrollIntoView({ behavior: "smooth", block: "center" });
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
    None: "#edf2f7"
  };
  let index = 0;
  sortedTags.forEach(([tag, count]) => {
    
    const tagItem = document.createElement("div");
    tagItem.className = "top-tag-item";
    tagShortcuts[index+1] = tag;
    index++;
    console.log(tag);
    
    
    console.log("here",tagShortcuts);
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
}
document.addEventListener("keydown", function (event) {
  let num = event.key;
  if (num >= "1" && num <= "5" && tagShortcuts[num]) {
    document.getElementById("tagSearch").value = tagShortcuts[num];
    assignTag();
  }
  // console.log(tagShortcuts[num]);
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
        console.log("here", data.taglist);
        autotaglist = data.taglist;
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

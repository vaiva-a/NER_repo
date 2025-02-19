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

function assignTag() {
  let selectedWordDiv = document.querySelector(".word.selected");
  if (!selectedWordDiv) {
    alert("Select a word first!");
    return;
  }
  let selectedTag = document.getElementById("tagSearch").value;
  if (!tags.includes(selectedTag)) {
    alert("Invalid tag!");
    return;
  }
  let sentenceIndex = selectedWordDiv.dataset.sentenceIndex;
  let wordIndex = selectedWordDiv.dataset.wordIndex;
  allTagData[sentenceIndex].annotations[wordIndex].tag = selectedTag;

  const tagColors = {
    person: "blue",
    location: "green",
    object: "orange",
    building: "brown",
    None: "#edf2f7",
  };

  selectedWordDiv.style.backgroundColor = tagColors[selectedTag] || "lightblue";
  selectedWordDiv.style.color = selectedTag === "None" ? "#2d3748" : "white";

  tagUsageCount[selectedTag] = (tagUsageCount[selectedTag] || 0) + 1;
  updateTopTags();
}

function updateTopTags() {
  let topTagsDiv = document.getElementById("topTagsList");
  topTagsDiv.innerHTML = "";
  let index = 0;
  // Sort tags by usage and get the top 5
  let topTags = Object.entries(tagUsageCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map((tag) => tag[0]);
  // Create buttons for top tags
  topTags.forEach((tag) => {
    let tagDiv = document.createElement("div");
    tagDiv.innerText = index + 1 + " - " + tag;
    tagDiv.classList.add("word");

    tagDiv.onclick = () => {
      document.getElementById("tagSearch").value = tag; // Update tagSearch
    };
    tagShortcuts[index + 1] = tag;
    index++;
    topTagsDiv.appendChild(tagDiv);
    console.log(tagShortcuts);
  });
}

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

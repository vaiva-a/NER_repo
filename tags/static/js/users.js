function deleteUser(username, role) {
    if (confirm(`Are you sure you want to delete ${role.toLowerCase()} ${username}?`)) {
      const endpoint = role === 'Annotator' ? '/remove_annotator/' : '/remove_validator/';
      
      fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ username: username })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert(data.message);
          const userCard = document.getElementById(`user-${username}`);
          if (userCard) {
            console.log("Deleted");
            userCard.remove();
          }
        } else {
          alert('Error: ' + data.message);
        }
      })
      .catch(error => {
        alert('Request failed: ' + error);
      });
    }
}

function openAddUserDialog() {
    document.getElementById("addUserDialog").style.display = "block";
}
function closeAddUserDialog() {
  document.getElementById("addUserDialog").style.display = "none";
  document.getElementById("addUserForm").reset();

  const radioButtons = document.querySelectorAll('input[name="userRole"]');
  radioButtons.forEach(radio => radio.checked = false);
}



function submitNewUser(event) {
  event.preventDefault();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const userRoleRadio = document.querySelector('input[name="userRole"]:checked');
  const userRole = userRoleRadio ? userRoleRadio.value : null;

  if (!userRole) {
    alert("Please select a user role!");
    return;
  }

  console.log("Submitting new user:", username, userRole);
  const endpoint = userRole === "annotator" ? "/add_annotator/" : "/add_validator/";
  console.log("Endpoint:", endpoint);
  

  fetch(endpoint, {
      method: "POST",
      body: JSON.stringify({
          username: username,
          password: password,
      }),
      headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': getCookie('csrftoken')

      },
  })
      .then((response) => response.json())
      .then((data) => {
          if (data.status === "success") {
              alert("User added successfully!");
              closeAddUserDialog();
              location.reload(); // Reload the page to show the new user
          } else {
              alert(data.message || "Error adding user!");
          }
      })
      .catch((error) => {
          console.error("Error:", error);
          alert("Failed to add user.");
      });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
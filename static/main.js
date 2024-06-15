$(document).ready(function () {
  let answers = {};

  function loadNextQuestion() {
    $.ajax({
      url: "/next_question",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(answers),
      success: function (response) {
        if (response.key === null) {
          $("#submit-btn").show();
          save_to_supabase(answers, userId);
          return;
        }

        let questionHtml = `<div class="question" data-key="${response.key}">
                    <p>${response.question}</p>`;

        if (response.options.length > 0) {
          response.options.forEach((option) => {
            questionHtml += `<label><input type="radio" name="${response.key}" value="${option}"> ${option}</label><br>`;
          });
        } else {
          questionHtml += `<input type="text" name="${response.key}">`;
        }

        questionHtml += `</div>`;
        $("#questions-container").append(questionHtml);
      },
    });
  }

  $(document).on("change", ".question input", function () {
    let key = $(this).closest(".question").data("key");
    let value = $(this).val();
    answers[key] = value;

    $(this).closest(".question").nextAll().remove(); // Remove following questions
    loadNextQuestion(); // Load the next question
  });

  $("#questionnaire-form").submit(function (e) {
    e.preventDefault();
    // Handle form submission
    let formData = new FormData(this);
    $.ajax({
      url: "/next_question",
      method: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function () {
        answers = {}; // Reset answers for new submission
        $("#questions-container").empty(); // Clear questions
        $("#submit-btn").hide(); // Hide submit button
        loadNextQuestion(); // Load first question again
      },
    });
  });

  loadNextQuestion(); // Initial load
});

function showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'block';
  }
  
  function showSignupModal() {
    const modal = document.getElementById('signupModal');
    modal.style.display = 'block';
  }
  
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
  }
  
  function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
  
    const data = { email, password, action: 'login' };
  
    $.ajax({
      url: '/authenticate',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(response) {
        if (response.success) {
          userId = response.user_id;
          closeModal('loginModal');
          loadNextQuestion();
        } else {
          alert(response.error);
        }
      },
      error: function() {
        alert('An error occurred during login.');
      }
    });
  }
  
  function signup() {
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
  
    const data = { email, password, action: 'signup' };
  
    $.ajax({
      url: '/authenticate',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(response) {
        if (response.success) {
          userId = response.user_id;
          closeModal('signupModal');
          loadNextQuestion();
        } else {
          alert(response.error);
        }
      },
      error: function() {
        alert('An error occurred during signup.');
      }
    });
  }

document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector(".form");
    var submitButton = document.querySelector(".submitButton");
    var loadingAnimation = document.getElementById("loadingAnimation");
  
    form.addEventListener("submit", function(event) {
      // Prevent the default form submission
      event.preventDefault();
  
      // Show the loading animation
      loadingAnimation.classList.remove("hidden");
  
      // Disable the submit button to prevent multiple submissions
      submitButton.disabled = true;
  
      // Simulate a delay for the animation (you can adjust the delay time)
      setTimeout(function() {
        // Enable the submit button
        submitButton.disabled = false;
  
        // Hide the loading animation
        loadingAnimation.classList.add("hidden");
  
        // Proceed with the form submission
        form.submit();
      }, 2000); // 2000 milliseconds (2 seconds) delay
    });
  });
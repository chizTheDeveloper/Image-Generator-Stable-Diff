document
  .getElementById("submit-btn")
  .addEventListener("click", async function () {
    const prompt = document.querySelector("input").value;
    const generatedImg = document.getElementById("generated-img");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.querySelector(".progress-container");

    if (!prompt) {
      alert("Please enter a prompt!");
      return;
    }

    // Show loading bar
    progressBar.style.width = "0%"; // Reset progress bar
    progressBar.parentElement.style.display = "block"; // Show progress bar

    const eventSource = new EventSource("http://localhost:8000/generate/");

    function updateProgressBar() {
      let width = 0;
      const interval = setInterval(() => {
        if (width >= 100) {
          clearInterval(interval);
        } else {
          width += 5; // Increase progress by 5% every 200ms
          progressBar.style.width = width + "%";
        }
      }, 200);
    }

    try {
      updateProgressBar(); // Start animation

      // Send request to generate an image
      await fetch("http://localhost:8000/generate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt }),
      });

      inputField.value = ""; // Clear input

      // Wait 2 seconds before fetching the latest image
      setTimeout(async () => {
        const latestResponse = await fetch(
          "http://localhost:8000/latest-image/"
        );
        const latestData = await latestResponse.json();

        if (latestResponse.ok) {
          generatedImg.src = `http://localhost:8000${latestData.image_url}`;
          generatedImg.style.display = "block";
        } else {
          console.error("Error fetching latest image:", latestData.error);
          alert("Failed to retrieve latest image.");
        }

        // Hide progress bar after completion
        progressBar.style.width = "100%";
        setTimeout(() => (progressContainer.style.display = "none"), 500);
      }, 2000);
    } catch (error) {
      console.error("Error:", error);
      alert("Image generation failed. Check server logs.");
      progressContainer.style.display = "none"; // Hide progress bar on error
    }
  });

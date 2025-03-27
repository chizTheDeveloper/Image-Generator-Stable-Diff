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

    // Reset UI
    progressBar.style.width = "0%";
    progressContainer.style.display = "block";
    generatedImg.style.display = "none"; // Hide old image

    try {
      const response = await fetch("http://localhost:8000/generate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt }),
      });

      if (!response.body) {
        throw new Error("No response body received");
      }

      const reader = response.body.getReader();
      let decoder = new TextDecoder();
      let imageUrl = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const progressMatch = chunk.match(/data: (\d+),?\s?(.*)?/);

        if (progressMatch) {
          let progress = parseInt(progressMatch[1], 10);
          progressBar.style.width = progress + "%";

          if (progress === 100 && progressMatch[2]) {
            imageUrl = progressMatch[2].trim(); // Extract the image URL
          }
        }
      }

      if (imageUrl) {
        // Force refresh by appending timestamp
        generatedImg.src = `http://localhost:8000${imageUrl}?t=${new Date().getTime()}`;
        generatedImg.style.display = "block";
      } else {
        alert("Failed to retrieve image URL.");
      }

      // Hide progress bar after completion
      setTimeout(() => {
        progressContainer.style.display = "none";
      }, 500);
    } catch (error) {
      console.error("Error:", error);
      alert("Image generation failed. Check server logs.");
      progressContainer.style.display = "none";
    }
  });

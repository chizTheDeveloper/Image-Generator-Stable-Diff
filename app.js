document
  .getElementById("submit-btn")
  .addEventListener("click", async function () {
    const prompt = document.querySelector("input").value;
    if (!prompt) {
      alert("Please enter a prompt!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/generate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt }),
      });

      if (!response.ok) throw new Error("Failed to generate image");

      const result = await response.json();
      const imageUrl = result.image_url;

      // Display the generated image
      document.querySelector(
        ".img-sec"
      ).innerHTML = `<img src="http://localhost:8000/${imageUrl}" alt="Generated Image">`;
    } catch (error) {
      console.error("Error:", error);
      alert("Image generation failed. Check the server logs.");
    }
  });

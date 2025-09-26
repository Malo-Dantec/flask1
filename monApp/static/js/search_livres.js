document.addEventListener("DOMContentLoaded", () => {
      const input = document.getElementById("search-input");
      const resultsContainer = document.getElementById("results");

      if (!input) return;

      input.addEventListener("keyup", async () => {
        const query = input.value;

        try {
          const response = await fetch(`/livres?q=${encodeURIComponent(query)}`);
          const html = await response.text();

          // Extraire seulement la partie résultats
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newResults = doc.querySelector("#results").innerHTML;

          resultsContainer.innerHTML = newResults;
        } catch (error) {
          console.error("Erreur recherche dynamique:", error);
        }
      });
    });
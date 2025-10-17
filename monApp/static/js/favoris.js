document.addEventListener("DOMContentLoaded", () => {
    const favoriBtns = document.querySelectorAll(".favori-btn");

    favoriBtns.forEach(btn => {
        btn.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const livreId = btn.getAttribute("data-livre-id");
            
            try {
                const response = await fetch(`/favoris/toggle/${livreId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    btn.textContent = data.est_favori ? "⭐" : "☆";
                }
            } catch (error) {
                console.error("Erreur lors de la modification du favori:", error);
            }
        });
    });
});
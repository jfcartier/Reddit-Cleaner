let currentId = null;

function loadNext() {
    fetch("/next")
        .then(res => res.json())
        .then(data => {
            if (data.done) {
                document.getElementById("comment-box").innerHTML = "<p class='text-center text-xl font-bold mt-4'>Fini!</p>";
                return;
            }
            
            // Mise à jour des données du commentaire
            currentId = data.id;
            document.getElementById("comment-body").innerText = data.body;
            document.getElementById("subreddit-title").innerText = data.subreddit_title || data.subreddit;
            document.getElementById("comment-subreddit").innerText = "r/" + data.subreddit;
            document.getElementById("comment-date").innerText = new Date(data.created_utc * 1000).toLocaleString();
            
            // Afficher les upvotes
            const upvotes = document.getElementById("comment-upvotes");
            upvotes.innerText = data.ups || "0";
            
            // Thumbnail du subreddit
            const thumb = document.getElementById("subreddit-thumb");
            if (data.subreddit_icon && data.subreddit_icon.trim() !== "") {
                thumb.src = data.subreddit_icon;
                thumb.style.display = "block";
            } else {
                thumb.src = "/static/default-icon.png";
                thumb.style.display = "block";
            }
            
            // Afficher le titre du post et le lien
            const postTitle = document.getElementById("post-title");
            const postLink = document.getElementById("post-link");
            
            if (data.post_title && data.post_title.trim() !== "") {
                postTitle.innerText = data.post_title;
                postLink.style.display = "block";
            } else {
                postTitle.innerText = "Commentaire Reddit";
                postLink.style.display = "block";
            }
            
            if (data.post_url && data.post_url.trim() !== "") {
                postLink.href = data.post_url;
            } else {
                postLink.href = "https://reddit.com/r/" + data.subreddit;
            }

            console.log("Données reçues:", data);
        })
        .catch(error => {
            console.error("Erreur lors du chargement:", error);
            document.getElementById("comment-body").innerText = "Erreur de chargement";
        });
}

function keep() {
    loadNext();
}

function remove() {
    fetch("/delete", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: currentId })
    })
    .then(() => loadNext())
    .catch(error => {
        console.error("Erreur lors de la suppression:", error);
        alert("Erreur lors de la suppression du commentaire");
    });
}

window.onload = loadNext;

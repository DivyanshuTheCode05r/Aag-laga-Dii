// Demo data (replace with TMDb later)
const demoMovies = [
  { title: "Inception", year: 2010, rating: 8.8, poster: "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg", genre: "Sci‑Fi" },
  { title: "Interstellar", year: 2014, rating: 8.6, poster: "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", genre: "Sci‑Fi" },
  { title: "The Dark Knight", year: 2008, rating: 9.0, poster: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", genre: "Action" },
  { title: "La La Land", year: 2016, rating: 8.0, poster: "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg", genre: "Drama" },
  { title: "Spirited Away", year: 2001, rating: 8.6, poster: "https://image.tmdb.org/t/p/w500/oRvMaJOmapypFUcQqpgHMZA6qL9.jpg", genre: "Fantasy" },
  { title: "Dune: Part Two", year: 2024, rating: 8.8, poster: "https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg", genre: "Sci‑Fi" },
  { title: "Oppenheimer", year: 2023, rating: 8.4, poster: "https://image.tmdb.org/t/p/w500/bAFmcrj7HEUfxAEPqPC48h2U6Jb.jpg", genre: "Drama" },
  { title: "John Wick", year: 2014, rating: 7.4, poster: "https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg", genre: "Action" },
  { title: "Your Name", year: 2016, rating: 8.4, poster: "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6babgKnONONX.jpg", genre: "Romance" },
  { title: "Parasite", year: 2019, rating: 8.6, poster: "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", genre: "Thriller" },
];

const grid = document.getElementById("grid");
const yearSpan = document.getElementById("year");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

function renderCards(list){
  grid.innerHTML = "";
  list.forEach(m => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = `
      <div class="card-media" style="background-image:url('${m.poster}')"></div>
      <div class="card-body">
        <h3 class="card-title">${m.title}</h3>
        <div class="card-meta">
          <span class="badge">${m.rating.toFixed(1)}</span>
          <span>•</span>
          <span>${m.year}</span>
          <span>•</span>
          <span>${m.genre}</span>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function filterMovies(query){
  const q = query.trim().toLowerCase();
  if(!q) return demoMovies;
  return demoMovies.filter(m =>
    m.title.toLowerCase().includes(q) ||
    String(m.year).includes(q) ||
    m.genre.toLowerCase().includes(q)
  );
}

// Initial render
renderCards(demoMovies);

// Search submit
searchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const list = filterMovies(searchInput.value);
  renderCards(list);
});

// Tag clicks
document.querySelectorAll(".tag").forEach(tag => {
  tag.addEventListener("click", () => {
    searchInput.value = tag.textContent;
    const list = filterMovies(tag.textContent);
    renderCards(list);
  });
});

// Year
yearSpan.textContent = new Date().getFullYear();

// Navbar hamburger
const hamburger = document.getElementById("hamburger");
const navMenu = document.getElementById("navMenu");
hamburger.addEventListener("click", () => {
  const isOpen = hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
  hamburger.setAttribute("aria-expanded", String(isOpen));
});
navMenu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => {
  hamburger.classList.remove("active");
  navMenu.classList.remove("active");
  hamburger.setAttribute("aria-expanded", "false");
}));

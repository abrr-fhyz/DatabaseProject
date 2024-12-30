let currentSystem = "ss";
async function filterData() {
  const filter = document.getElementById("coordinate-dropdown").value;
  currentSystem = filter;
  
}

function showImage(imageName) {
    const imagePath = `/Year-2 Semester-2/CSE 2201/Project/images/${imageName}.png`;
    const imgElement = document.getElementById("image-display");
    if (imgElement) {
        console.log(imagePath);
        imgElement.src = imagePath;
        imgElement.style.display = "block";
    } else {
        console.error("Element with id 'image-display' not found.");
    }
}

function getTelescopeData() {
    showImage('Telescope_discovery');
}

function getPlanetData() {
    showImage('planet_system');
}

function getStellarData() {
    showImage('stellerDist');
}

function coordinatePlot() {
    let name = "Coordinate_plot_";
    name += currentSystem;
    showImage(name);   
}

function searchView() {
    window.location.href = 'index.html';
}

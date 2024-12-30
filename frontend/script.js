const apiUrl = "http://127.0.0.1:5000/api";

document.getElementById("search-bar").addEventListener("input", filterData);

async function filterData() {
  const filter = document.getElementById("filter-dropdown").value;
  updateTableHead(filter)
  if (filter === "general") {
    generalSearch();
  } else {
    searchData(filter);
  }
}

function updateTableHead(filter) {
    const tableHead = document.getElementById("table-head");
    tableHead.innerHTML = "";
    let newHeadHTML = "";
    if (filter === "star") {
      newHeadHTML = `
        <tr>
          <th>Serial</th>
          <th>Star Name</th>
          <th>Stellar Class</th>
          <th>Solar Radius</th>
          <th>Solar Mass</th>
          <th>System</th>
          <th>Distance</th>
        </tr>
      `;
    } else if (filter === "planet") {
      newHeadHTML = `
        <tr>
          <th>Serial</th>
          <th>Planet Name</th>
          <th>Parent System</th>
          <th>Planetary Radius</th>
          <th>Planetary Mass</th>
          <th>Orbital Period</th>
          <th>Atmosphere</th>
        </tr>
      `;
    } else if (filter === "misc") {
      newHeadHTML = `
        <tr>
          <th>Serial</th>
          <th>Object Name</th>
          <th>Object Location</th>
          <th>Object Category</th>
          <th>Object Distance</th>
        </tr>
      `;
    } else {
      newHeadHTML = `
        <tr>
          <th>Serial</th>
          <th>Object Name</th>
          <th>Object Location</th>
          <th>Category</th>
          <th>Discovering Telescope</th>
          <th>Discovery Year</th>
        </tr>
      `;
    }
    tableHead.innerHTML = newHeadHTML;
  }

async function generalSearch() {
  const keyword = document.getElementById("search-bar").value.trim();
  if (!keyword) {
    return;
  }

  const response = await fetch(`${apiUrl}/generalSearch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keyword: keyword
    }),
  });

  if (!response.ok) {
    console.error('Error in the request:', response.statusText);
    return;
  }

  const data = await response.json(); 

  const dataList = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  dataList.innerHTML = "";
  let sl = 1;
  data.forEach(item => {
        const row = document.createElement("tr");
        const slCell = document.createElement("td");
        slCell.textContent = sl++;

        const objCell = document.createElement("td");
        objCell.textContent = item.obj_name;

        const categoryCell = document.createElement("td");
        categoryCell.textContent = item.obj_type;

        const locCell = document.createElement("td");
        locCell.textContent = item.obj_loc;

        const telescopeCell = document.createElement("td");
        telescopeCell.textContent = item.telescope;

        const yearCell = document.createElement("td");
        yearCell.textContent = item.discovery;

        row.appendChild(slCell);
        row.appendChild(objCell);
        row.appendChild(categoryCell);
        row.appendChild(locCell);
        row.appendChild(telescopeCell);
        row.appendChild(yearCell);
        dataList.appendChild(row);
      });
}

async function searchData(filter) {
  const keyword = document.getElementById("search-bar").value.trim();
  if (!keyword) {
    return;
  }

  const response = await fetch(`${apiUrl}/specifiedSearch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keyword: keyword,
      filter: filter
    }),
  });

  if (!response.ok) {
    console.error('Error in the request:', response.statusText);
    return;
  }

  const data = await response.json(); 

  if(filter == "star"){
    showStarData(data);
  }
  if(filter == "planet"){
    showPlanetData(data);
  }
  if(filter == "misc"){
    showMiscData(data);
  }
}

function showStarData(data) {
  const dataList = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  dataList.innerHTML = "";
  let sl = 1;
  data.forEach(item => {
        const row = document.createElement("tr");
        const slCell = document.createElement("td");
        slCell.textContent = sl++;

        const starCell = document.createElement("td");
        starCell.textContent = item.star_name;

        const classCell = document.createElement("td");
        classCell.textContent = item.stellar_class;

        const radiiCell = document.createElement("td");
        radiiCell.textContent = item.solar_radii;

        const massCell = document.createElement("td");
        massCell.textContent = item.solar_mass;

        const systemCell = document.createElement("td");
        systemCell.textContent = item.star_type;

        const distCell = document.createElement("td");
        distCell.textContent = item.distance;

        row.appendChild(slCell);
        row.appendChild(starCell);
        row.appendChild(classCell);
        row.appendChild(radiiCell);
        row.appendChild(massCell);
        row.appendChild(systemCell);
        row.appendChild(distCell);
        
        dataList.appendChild(row);
      });
}

function showPlanetData(data) {
  const dataList = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  dataList.innerHTML = "";
  let sl = 1;
  data.forEach(item => {
        const row = document.createElement("tr");
        const slCell = document.createElement("td");
        slCell.textContent = sl++;

        const planetCell = document.createElement("td");
        planetCell.textContent = item.planet_name;

        const parentCell = document.createElement("td");
        parentCell.textContent = item.parent_system;

        const radiiCell = document.createElement("td");
        radiiCell.textContent = item.planet_radius;

        const massCell = document.createElement("td");
        massCell.textContent = item.planet_mass;

        const orbitCell = document.createElement("td");
        orbitCell.textContent = item.orbit;

        const atmCell = document.createElement("td");
        atmCell.textContent = item.atmosphere;

        row.appendChild(slCell);
        row.appendChild(planetCell);
        row.appendChild(parentCell);
        row.appendChild(radiiCell);
        row.appendChild(massCell);
        row.appendChild(orbitCell);
        row.appendChild(atmCell);
        
        dataList.appendChild(row);
      });
}

function showMiscData(data) {
  const dataList = document.getElementById("results-table").getElementsByTagName("tbody")[0];
  dataList.innerHTML = "";
  let sl = 1;
  data.forEach(item => {
        const row = document.createElement("tr");
        const slCell = document.createElement("td");
        slCell.textContent = sl++;

        const miscCell = document.createElement("td");
        miscCell.textContent = item.misc_name;

        const parentCell = document.createElement("td");
        parentCell.textContent = item.parent_system;

        const categoryCell = document.createElement("td");
        categoryCell.textContent = item.misc_category;

        const distCell = document.createElement("td");
        distCell.textContent = item.distance;

        row.appendChild(slCell);
        row.appendChild(miscCell);
        row.appendChild(parentCell);
        row.appendChild(categoryCell);
        row.appendChild(distCell);
        
        dataList.appendChild(row);
      });
}

function switchToImageView() {
    window.location.href = 'analysis_view.html'; 
}

<template>
  <div>
    <!-- Map -->
    <svg id="map" width="100%" height="600"></svg>

    <!-- Legend -->
    <div id="legend"></div>
    
    <!-- Controls -->
    <div id="controls">
      <div id="regionSelectorContainer">
        <label for="regionSelector">Select Region:</label>
        <select id="regionSelector">
          <option disabled>Zoom to selection</option>
          <option selected value="world">World</option>
          <option value="africa">Africa</option>
          <option value="asia">Asia</option>
          <option value="europe">Europe</option>
          <option value="northAmerica">North America</option>
          <option value="middleAmerica">Middle America</option>
          <option value="southAmerica">South America</option>
          <option value="oceania">Oceania</option>
        </select>
      </div>
      <button id="playButton">Play</button>
      <input type="range" id="yearSlider" min="1960" max="2023" value="2010" step="1">
      <span id="yearLabel">2010</span>
    </div>

    <!-- Tooltip -->
    <div id="tooltip" class="tooltip" style="opacity: 0;"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
export default {
  mounted() {
    const width = 1200, height = 560;
    let currentRegion = "world";
    const yearSlider = d3.select("#yearSlider");
    const yearLabel = d3.select("#yearLabel");
    const tooltip = d3.select("#tooltip");

    // Projection and path generator
    const projection = d3.geoMercator().scale(150).translate([width / 2, height / 2]);
    const path = d3.geoPath().projection(projection);

    // Color scale for GDP
    const colorScale = d3.scaleThreshold()
      .domain([-1, 0, 1000, 5000, 10000, 20000, 50000])
      .range(["#cccccc", "#f2f2f2", "#d9f0a3", "#addd8e", "#78c679", "#41ab5d", "#238443", "#004529"]);

    // Legend
    const legendLabels = [
      ["No data", -1], 
      ["$0", 0], 
      ["$1,000", 1000], 
      ["$5,000", 5000], 
      ["$10,000", 10000], 
      ["$20,000", 20000], 
      ["$50,000+", 50000]
    ];
    const legend = d3.select("#legend");
    
    const legendContainer = legend.append("div")
      .style("display", "flex")
      .style("align-items", "flex-start")
      .style("margin-top", "2%")

    legendLabels.forEach((d, i) => {
      const item = legendContainer.append("div")
        .attr("class", "legend-item")
        .on("click", function() {
          const isSelected = d3.select(this).classed("selected");
          legendContainer.selectAll(".legend-item").classed("selected", false);
          svg.selectAll("path")
            .classed("dimmed", false)
            .classed("country-highlight", false);
          if (!isSelected) {
            d3.select(this).classed("selected", true);
            highlightRange(d[0] === "No data" ? d[0] : d[1]);
          }
        });

      item.append("div")
        .attr("class", "legend-label")
        .text(d[0]);

      item.append("div")
        .attr("class", "legend-bar")
        .style("background", d[0] === "No data" ? "#cccccc" : colorScale(d[1]));

      // Add arrow only after the last item
      if (i === legendLabels.length - 1) {
        item.append("div")
          .attr("class", "legend-arrow")
          .style("border-left-color", colorScale(d[1]));
      }

      // Add gap after "No data"
      if (i === 0) {
        legendContainer.append("div")
          .attr("class", "legend-gap")
          .style("width", "20px");
      }
    });

    function highlightRange(range) {
      svg.selectAll("path")
        .attr("class", d => {
          const countryData = gdpData.get(+yearSlider.property("value")).get(d.id);
          if (range === "No data") {
            return countryData === undefined || countryData === "" || countryData === 0 ? "country-highlight" : "country dimmed";
          } else {
            const [min, max] = getRangeBounds(range);
            return countryData >= min && countryData < max ? "country-highlight" : "country dimmed";
          }
        });
    }

    function getRangeBounds(range) {
      switch (range) {
        case 0: return [1, 1000];
        case 1000: return [1000, 5000];
        case 5000: return [5000, 10000];
        case 10000: return [10000, 20000];
        case 20000: return [20000, 50000];
        case 50000: return [50000, Infinity];
        default: return [-Infinity, Infinity];
      }
    }

    // Data storage
    let worldData, gdpData = new Map();

    // Load data
    Promise.all([
      d3.json("data/worlddata.json"),
      d3.csv("data/gdpdata.csv", d => {
        for (let year = 1960; year <= 2023; year++) {
          if (!gdpData.has(year)) gdpData.set(year, new Map());
          gdpData.get(year).set(d["Country Code"], +d[year]);
        }
      })
    ]).then(data => {
      worldData = data[0];
      updateMap(2010);

      // Event listeners
      yearSlider.on("input", function() {
        const selectedYear = +this.value;
        yearLabel.text(selectedYear);
        updateMap(selectedYear);
      });

      d3.select("#regionSelector").on("change", function() {
        currentRegion = this.value;
        updateMap(+yearSlider.property("value"));
      });
    });

    // Map update function
    const svg = d3.select("#map");
    function updateMap(year) {
      const regionBounds = {
        world: [[-180, -60], [180, 85]],
        africa: [[-20, -35], [40, 35]],
        asia: [[50, -10], [80, 50]],
        europe: [[-20, 30], [50, 60]],
        northAmerica: [[-170, 5], [-50, 75]],
        middleAmerica: [[-120, 8], [-60, 30]],
        southAmerica: [[-90, -60], [-30, 15]],
        oceania: [[105, -50], [180, 10]],
      };

      // Filter and adjust projection
      const bounds = regionBounds[currentRegion];
      if (bounds) projection.fitExtent([[50, 50], [1150, 550]], { type: "Polygon", coordinates: [[
        [bounds[0][0], bounds[0][1]],
        [bounds[0][0], bounds[1][1]],
        [bounds[1][0], bounds[1][1]],
        [bounds[1][0], bounds[0][1]],
        [bounds[0][0], bounds[0][1]]
      ]]});

      svg.selectAll("path")
        .data(worldData.features)
        .join("path")
        .attr("d", path)
        .attr("fill", d => {
          const countryData = gdpData.get(year).get(d.id);
          return countryData !== undefined && countryData !== "" && countryData !== 0 ? colorScale(countryData) : "#ccc";
        })
        .attr("class", "country")
        .on("mouseover", function(event, d) {
          if (!d3.select(".legend-item.selected").empty()) return;
          d3.select(this).classed("country-highlight", true);
          svg.selectAll("path").classed("dimmed", true);
          d3.select(this).classed("dimmed", false);

          const countryData = gdpData.get(year).get(d.id);
          if (countryData !== undefined && countryData !== "" && countryData !== 0) {
            showTooltip(event, d, countryData);
          } else {
            showTooltip(event, d, 'No data');
          }
        })
        .on("mousemove", function(event) {
          tooltip.style("left", (event.pageX + 10) + "px")
                 .style("top", (event.pageY - 10) + "px");
        })
        .on("mouseout", function() {
          if (!d3.select(".legend-item.selected").empty()) return;
          d3.select(this).classed("country-highlight", false);
          svg.selectAll("path").classed("dimmed", false);
          hideTooltip();
        });
    }

    // Show Tooltip with Chart
    function showTooltip(event, d, countryData) {
      const years = Array.from(gdpData.keys()).filter(y => y >= 1960 && y <= 2023);
      const values = years.map(y => gdpData.get(y).get(d.id) || 0);
      const currentYear = +yearSlider.property("value");
      const currentValue = gdpData.get(currentYear).get(d.id) || 0;

      tooltip.html(`
        <div class="tooltip-header">
          <div class="tooltip-title">${d.properties.name}</div>
          <div class="tooltip-year">Year: ${currentYear}</div>
        </div>
        <div class="tooltip-content">
          <div class="tooltip-gdp">GDP per capita: $${Math.round(countryData).toLocaleString()}</div>
          <svg class="tooltip-chart"></svg>
        </div>
      `);

      const margin = { top: 10, right: 10, bottom: 20, left: 40 };
      const chartWidth = 200 - margin.left - margin.right;
      const chartHeight = 100 - margin.top - margin.bottom;

      const x = d3.scaleLinear()
        .domain([1960, 2023])
        .range([0, chartWidth]);

      const y = d3.scaleLinear()
        .domain([0, d3.max(values)])
        .range([chartHeight, 0]);

      const line = d3.line()
        .x((_, i) => x(+years[i]))
        .y(d => y(d))
        .curve(d3.curveMonotoneX);

      const chartSvg = tooltip.select("svg")
        .attr("width", chartWidth + margin.left + margin.right)
        .attr("height", chartHeight + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      // Add the line
      chartSvg.append("path")
        .datum(values)
        .attr("fill", "none")
        .attr("d", line);

      // Add current year point
      chartSvg.append("circle")
        .attr("cx", x(currentYear))
        .attr("cy", y(currentValue))
        .attr("r", 4);

      // Add axes
      chartSvg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0,${chartHeight})`)
        .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format("d")));

      chartSvg.append("g")
        .attr("class", "axis")
        .call(d3.axisLeft(y).ticks(5).tickFormat(d => `$${d3.format("~s")(d)}`));

      tooltip.style("opacity", 1)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
    }

    function hideTooltip() {
      tooltip.style("opacity", 0);
    }

    const playButton = d3.select("#playButton");
    let isPlaying = false;
    let playInterval;

    playButton.on("click", function() {
      if (isPlaying) {
        clearInterval(playInterval);
        playButton.text("Play");
      } else {
        playInterval = setInterval(() => {
          let currentYear = +yearSlider.property("value");
          if (currentYear < 2023) {
            yearSlider.property("value", currentYear + 1).dispatch("input");
          } else {
            clearInterval(playInterval);
            playButton.text("Play");
          }
        }, 1000);
        playButton.text("Pause");
      }
      isPlaying = !isPlaying;
    });
  }
};
</script>

<style>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    text-align: center;
    background-color: #f9f9f9;
  }
  h1 {
    margin: 20px;
    font-size: 24px;
  }
  svg {
    display: block;
    margin: 0 auto;
  }
  #controls {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px auto;
    position: relative;
    width: 60%;
    gap: 20px;
    background: rgba(255, 255, 255, 0.95);
    padding: 15px 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  #yearSlider {
    width: 45%;
    -webkit-appearance: none;
    appearance: none;
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(to right, #e8f5e9, #c8e6c9, #a5d6a7, #81c784, #66bb6a, #4caf50, #2e7d32);
    outline: none;
    cursor: pointer;
  }

  #yearSlider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #4CAF50;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
  }

  #yearSlider::-webkit-slider-thumb:hover {
    transform: scale(1.1);
    background: #45a049;
  }

  #regionSelectorContainer {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  #regionSelectorContainer label {
    font-weight: 500;
    color: #333;
  }

  #regionSelector {
    padding: 8px 12px;
    font-size: 14px;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    background-color: white;
    color: #333;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  #regionSelector:hover {
    border-color: #45a049;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  #regionSelector:focus {
    outline: none;
    border-color: #2d662f;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
  }

  #yearLabel {
    font-weight: 600;
    color: #2d662f;
    min-width: 45px;
    text-align: center;
  }
  #legend {
    display: flex;
    justify-content: center;
    margin-bottom: 3%;
    position: relative;
    flex-wrap: nowrap; /* Ensure legends are on the same line */
    align-items: flex-start; /* Ensure all items align from the top */
  }
  .legend-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Change from center to flex-start */
    position: relative;
    min-width: 80px;
    cursor: pointer;
  }
  .legend-bar {
    height: 20px;
    width: 100%;
    transition: opacity 0.2s;
  }
  .legend-item:hover .legend-bar {
    opacity: 0.8;
  }
  .legend-item.selected .legend-bar {
    outline: 2px solid #000;
    outline-offset: -2px;
  }
  .legend-arrow {
    position: absolute;
    right: -25%; /* Align to the right edge of the legend item */
    top: 45%; /* Center vertically */
    transform: translateY(-50%); /* Adjust for centering */
    width: 0;
    height: 0;
    border-left: 20px solid;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    z-index: 1;
  }
  .no-data-box {
    width: 60px;
    height: 20px;
    background: #cccccc;
    margin-right: 20px;
  }
  .tooltip {
    position: absolute;
    pointer-events: none;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    font-size: 13px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    min-width: 200px;
    max-width: 300px;
  }
  .tooltip-chart {
    width: 100%;
    height: 100px;
    margin-top: 10px;
    background-color: #fff;
  }
  .tooltip-chart path {
    stroke: #4299e1;
    stroke-width: 2;
  }
  .tooltip-chart circle {
    fill: #e53e3e;
    stroke: #fff;
    stroke-width: 2;
  }
  .tooltip-chart .axis text {
    font-size: 10px;
  }
  .tooltip-chart .axis path,
  .tooltip-chart .axis line {
    stroke: #cbd5e0;
  }
  .tooltip-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 20px; /* Add padding for visual separation */
      border-radius: 4px; /* Add border radius for rounded corners */
      background-color: rgba(255, 255, 255, 0.8); /* Light background for contrast */
  }
  .tooltip-title {
      font-weight: bold;
      font-size: 16px;
  }
  .tooltip-year {
      font-size: 12px; /* Slightly smaller font size */
      color: #555;
  }
  .tooltip-content {
      margin: 10px 0;
      padding: 0 12px; /* Add padding for consistency */
  }
.tooltip-gdp {
    font-size: 14px;
    color: #2c5282;
}
  .country-highlight {
    stroke: #333;
    stroke-width: 1;
  }
  #playButton {
    padding: 8px 20px;
    font-size: 16px;
    cursor: pointer;
    margin-right: 1.5%;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
  }
  #playButton:hover {
    background-color: #45a049;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    transform: translateY(-1px);
  }
  #playButton:active {
    transform: translateY(1px);
    box-shadow: 0 1px 2px rgba(0,0,0,0.2);
  }
  .no-data-item {
    display: flex;
    flex-direction: column;
    align-items: center; /* Align with other legend items */
    margin-right: 2%; /* Add cursor pointer for consistency */
  }

  .legend-label {
    margin-top: -20px;
    font-size: 12px;
    margin-left: 2px;
    text-align: left; /* Ensure text aligns left */
    width: 100%; /* Ensure label takes full width */
  }
  .legend-gap {
    width: 2%;
    height: 1px;
  }
  .legend-item:first-child .legend-label {
    text-align: center;
    margin-left: 0;
  }
  .country {
    fill-opacity: 1;
    transition: fill-opacity 0.2s;
  }
  .country.dimmed {
    fill-opacity: 0.2;
  }
</style>
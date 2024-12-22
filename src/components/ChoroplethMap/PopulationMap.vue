<template>
  <div>
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
      <input type="range" id="yearSlider" min="1960" max="2021" value="2010" step="1">
      <span id="yearLabel">2010</span>
    </div>
    
    <!-- Map -->
    <svg id="map" width="100%" height="600"></svg>

    <!-- Legend -->
    <div id="legend"></div>

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

    // Color scale for Population
    const colorScale = d3.scaleThreshold()
      .domain([-1, 1, 1e5, 1e6, 1e7, 1e8, 1e9])
    .range(["#cccccc", "#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#084594"]);

    // Legend
    const legendLabels = [
      ["No data", -1],
      ["< 100K", 1], 
      ["100K - 1M", 1e5], 
      ["1M - 10M", 1e6], 
      ["10M - 100M", 1e7], 
      ["100M - 500M", 1e8], 
      ["500M+", 1e9], 
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

      // Add gap after first item
      if (i === 0) {
        legendContainer.append("div")
          .attr("class", "legend-gap")
          .style("width", "20px");
      }
    });

    function highlightRange(range) {
      svg.selectAll("path")
        .attr("class", d => {
          const countryData = populationData.get(+yearSlider.property("value")).get(d.id);
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
        case -1: return [-Infinity, 0];
        case 1: return [0, 1e5];
        case 1e5: return [1e5, 1e6];
        case 1e6: return [1e6, 1e7];
        case 1e7: return [1e7, 1e8];
        case 1e8: return [1e8, 5e8];
        case 1e9: return [1e9, 1.5e9];
        default: return [-Infinity, Infinity];
      }
    }

    // Data storage
    let worldData, populationData = new Map();

    // Load data
    Promise.all([
      d3.json("data/worlddata.json"),
      d3.csv("data/world-population.csv", d => {
        for (let year = 1960; year <= 2021; year++) {
          if (!populationData.has(year)) populationData.set(year, new Map());
          populationData.get(year).set(d["Country Code"], +d[year]);
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
          const countryData = populationData.get(year).get(d.id);
          return countryData !== undefined && countryData !== "" && countryData !== 0 ? colorScale(countryData) : "#ccc";
        })
        .attr("class", "country")
        .on("mouseover", function(event, d) {
          if (!d3.select(".legend-item.selected").empty()) return;
          d3.select(this).classed("country-highlight", true);
          svg.selectAll("path").classed("dimmed", true);
          d3.select(this).classed("dimmed", false);

          const countryData = populationData.get(year).get(d.id);
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
      const years = Array.from(populationData.keys()).filter(y => y >= 1960 && y <= 2021);
      const values = years.map(y => populationData.get(y).get(d.id) || 0);
      const currentYear = +yearSlider.property("value");
      const currentValue = populationData.get(currentYear).get(d.id) || 0;

      tooltip.html(`
        <div class="tooltip-header">
          <div class="tooltip-title">${d.properties.name}</div>
          <div class="tooltip-year">Year: ${currentYear}</div>
        </div>
        <div class="tooltip-content">
          <div class="tooltip-population">Population: ${Math.round(countryData).toLocaleString()}</div>
          <svg class="tooltip-chart"></svg>
        </div>
      `);

      const margin = { top: 10, right: 10, bottom: 20, left: 40 };
      const chartWidth = 200 - margin.left - margin.right;
      const chartHeight = 100 - margin.top - margin.bottom;

      const x = d3.scaleLinear()
        .domain([1960, 2021])
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
        .call(d3.axisLeft(y).ticks(5).tickFormat(d => d3.format("~s")(d)));

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
          if (currentYear < 2021) {
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


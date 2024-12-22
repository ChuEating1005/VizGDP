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
        <input type="range" id="yearSlider" min="2005" max="2023" value="2010" step="1">
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
  
      // Color scale for GDP
    const colorScale = d3.scaleThreshold()
      .domain([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
      .range(["#cccccc", "#800000", "#cc0000", "#ff8000", "#ffcc00", "#41ab5d", "#238443", "#004529"]);

    // Legend
    const legendLabels = [
      ["No data", "No data"],
      ["1.0-1.9", 1.0],
      ["2.0-2.9", 2.0],
      ["3.0-3.9", 3.0],
      ["4.0-4.9", 4.0],
      ["5.0-5.9", 5.0],
      ["6.0-6.9", 6.0],
      ["7.0+", 7.0]
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
            const countryData = gnhData.get(+yearSlider.property("value")).get(d.id);
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
          case 1.0: return [1.0, 2.0];
          case 2.0: return [2.0, 3.0];
          case 3.0: return [3.0, 4.0];
          case 4.0: return [4.0, 5.0];
          case 5.0: return [5.0, 6.0];
          case 6.0: return [6.0, 7.0];
          case 7.0: return [7.0, Infinity];
          default: return [-Infinity, Infinity];
        }
      }
  
      // Data storage
      let worldData, gnhData = new Map();
  
      // Load data
      Promise.all([
        d3.json("data/worlddata.json"),
        d3.csv("data/gnhdata.csv", d => {
          for (let year = 2005; year <= 2023; year++) {
            if (!gnhData.has(year)) gnhData.set(year, new Map());
            gnhData.get(year).set(d["Country Code"], +d[year]);
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
            const countryData = gnhData.get(year).get(d.id);
            return countryData !== undefined && countryData !== "" && countryData !== 0 ? colorScale(countryData) : "#ccc";
          })
          .attr("class", "country")
          .on("mouseover", function(event, d) {
            if (!d3.select(".legend-item.selected").empty()) return;
            d3.select(this).classed("country-highlight", true);
            svg.selectAll("path").classed("dimmed", true);
            d3.select(this).classed("dimmed", false);
  
            const countryData = gnhData.get(year).get(d.id);
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
        const years = Array.from(gnhData.keys()).filter(y => y >= 2005 && y <= 2023);
        const values = years.map(y => gnhData.get(y).get(d.id) || 0);
        const currentYear = +yearSlider.property("value");
        const currentValue = gnhData.get(currentYear).get(d.id) || 0;
  
        tooltip.html(`
          <div class="tooltip-header">
            <div class="tooltip-title">${d.properties.name}</div>
            <div class="tooltip-year">Year: ${currentYear}</div>
          </div>
          <div class="tooltip-content">
            <div class="tooltip-gnh">GNH (ladder score): ${typeof countryData === 'number' ? countryData.toFixed(2).toLocaleString() : countryData}</div>
            <svg class="tooltip-chart"></svg>
          </div>
        `);
  
        const margin = { top: 10, right: 10, bottom: 20, left: 40 };
        const chartWidth = 200 - margin.left - margin.right;
        const chartHeight = 100 - margin.top - margin.bottom;
  
        const x = d3.scaleLinear()
          .domain([2005, 2023])
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
          .call(d3.axisLeft(y).ticks(5).tickFormat(d => `${d3.format("~s")(d)}`));
  
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
  
  
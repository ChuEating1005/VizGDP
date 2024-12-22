<template>
  <div>
    <div class="region-selector flex">
      <label><strong>Select Regions:</strong></label>
      <div v-for="region in availableRegions" :key="region" class="region-checkbox">
        <div
          :style="{ backgroundColor: regionColors[region] || '#cccccc' }"
          class="region-color-block"
          @click="toggleRegion(region)"
        ></div>
        <span class="ml-1">{{ region }}</span>
      </div>
    </div>
    <div id="scatterplot" class="scatterplot-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'ScatterPlotChart',
  data() {
    return {
      allData: [], // Store all data loaded from CSV
      selectedRegions: [], // User-selected regions
      availableRegions: [], // All unique regions in the data
      chart: null, // Add chart instance to component data
      regionColors: {
        Oceania: '#21aa49',
        Africa: '#020307',
        Europe: '#0881c2',
        Americas: '#e31c22',
        Asia: '#f6d007'
      }
    };
  },
  mounted() {
    this.loadDataAndRenderChart();
  },
  beforeDestroy() {
    // Clean up chart instance
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    async loadDataAndRenderChart() {
      try {
        const response = await axios.get('data/GNH_2023.csv');
        const csvData = response.data;
        const parsedData = this.parseCSV(csvData);

        // Store all data and extract unique regions
        this.allData = parsedData;
        this.availableRegions = [
          ...new Set(parsedData.map(d => d.region).filter(Boolean)),
        ];

        // Initially select all regions
        this.selectedRegions = [...this.availableRegions];

        // Initialize chart once
        this.initializeChart();
        this.updateChart();
      } catch (error) {
        console.error('Error loading data:', error);
      }
    },
    parseCSV(csvData) {
      const rows = csvData.split('\n');
      const headers = rows[0].split(',');
      const data = rows.slice(1).map(row => {
        const values = row.split(',').map(v => (v === '' ? null : v.trim()));
        while (values.length < headers.length) {
          values.push(null); // Ensure correct alignment by filling missing values with null
        }
        const entry = headers.reduce((acc, header, index) => {
          acc[header.trim()] = values[index];
          return acc;
        }, {});
        return {
          name: entry['Country name'] || null,
          year: entry['year'] || null,
          lifeLadder: entry['Life Ladder'] ? parseFloat(entry['Life Ladder']) : null,
          logGDP: entry['Log GDP per capita'] ? parseFloat(entry['Log GDP per capita']) : null,
          socialSupport: entry['Social support'] ? parseFloat(entry['Social support']) : null,
          healthyLife: entry['Healthy life expectancy at birth'] ? parseFloat(entry['Healthy life expectancy at birth']) : null,
          freedom: entry['Freedom to make life choices'] ? parseFloat(entry['Freedom to make life choices']) : null,
          generosity: entry['Generosity'] ? parseFloat(entry['Generosity']) : null,
          corruption: entry['Perceptions of corruption'] ? parseFloat(entry['Perceptions of corruption']) : null,
          positiveAffect: entry['Positive affect'] ? parseFloat(entry['Positive affect']) : null,
          negativeAffect: entry['Negative affect'] ? parseFloat(entry['Negative affect']) : null,
          region: entry['Region'] || null,
          code: entry['Country Code'] || null,
          population: entry['2021'] ? parseInt(entry['2021'], 10) : null,
        };
      });
      return data;
    },
    initializeChart() {
      this.chart = echarts.init(document.getElementById('scatterplot'));
      
      const regionColors = {
        Oceania: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#2ecc71' },
          { offset: 1, color: '#27ae60' }
        ]),
        Africa: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#34495e' },
          { offset: 1, color: '#2c3e50' }
        ]),
        Europe: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#3498db' },
          { offset: 1, color: '#2980b9' }
        ]),
        Americas: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#e74c3c' },
          { offset: 1, color: '#c0392b' }
        ]),
        Asia: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#f1c40f' },
          { offset: 1, color: '#f39c12' }
        ])
      };

      // Add label position checking
      const labelLayout = {
        hideOverlap: true,
        moveOverlap: 'shiftX'
      };

      // Transform all data once
      const seriesData = this.allData.map(d => ({
        value: [d.logGDP, d.lifeLadder],
        symbolSize: d.population ? Math.sqrt(Math.sqrt(d.population)) / 2 : 10,
        itemStyle: {
          color: regionColors[d.region] || '#cccccc',
          opacity: this.selectedRegions.includes(d.region) ? 1 : 0,
          borderColor: '#fff',
          borderWidth: .1,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
        label: {
          show: false, // Hide labels by default
          color: 'gray',
          position: 'top',
          distance: 5,
          formatter: d.code
        },
        originalData: d,
        z: d.population ? Math.sqrt(d.population) : 1,
      }));

      this.chart.setOption({
        backgroundColor: '#f8f9fa',
        animation: true,
        animationDuration: 500,
        animationEasing: 'quadraticInOut',
        animationThreshold: 2000,
        title: {
          text: '',
          left: 'center',
          top: 'top',
          textStyle: {
            color: '#2c3e50',
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        grid: {
          left: '10%',
          right: '10%',
          top: '10%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: {
          name: 'Log GDP per Capita',
          type: 'value',
          min: 7,
          max: 12,
            nameTextStyle: { 
            color: '#2c3e50',
            fontSize: 14,
            align: 'center',
            verticalAlign: 'top',
            padding: [30, 0, 0, -30],
            fontWeight: 'bold'
            },
          axisLabel: { 
            color: '#2c3e50',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(0,0,0,0.1)',
              type: 'dashed'
            }
          }
        },
        yAxis: {
          name: 'Life Ladder',
          type: 'value',
          min: 2,
          nameTextStyle: { 
            color: '#2c3e50',
            fontSize: 14,
            fontWeight: 'bold'
          },
          axisLabel: { 
            color: '#2c3e50',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(0,0,0,0.1)',
              type: 'dashed'
            }
          }
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(255,255,255,0.9)',
          borderWidth: 1,
          padding: 10,
          textStyle: {
            color: '#333'
          },
          formatter: function (params) {
            const item = params.data.originalData;
            const borderColor = params.data.itemStyle.color;
            return `
              <div style="font-weight:bold; border-left: 4px solid ${borderColor}; padding-left: 8px;">
                ${item.name} (${item.code})
              </div>
              <div>Region: ${item.region}</div>
              <div>Log GDP: ${params.value[0].toFixed(2)}</div>
              <div>Life Ladder: ${params.value[1].toFixed(2)}</div>
              <div>Population: ${item.population?.toLocaleString()}</div>
            `;
          }
        },
        legend: {
          data: Object.keys(regionColors),
          textStyle: { color: '#2c3e50' },
          selectedMode: false,
          bottom: 10
        },
        series: [{
          type: 'scatter',
          data: seriesData,
          label: {
            show: false, // Hide labels by default
            color: '#2c3e50', // Set a single color for all labels
            fontSize: 10,
            fontWeight: 'bold',
            formatter: function (params) {
              // Only show label if point is visible and not overlapping
              if (params.data.itemStyle.opacity === 0 || params.data.labelLayout.hideOverlap) return '';
              return params.data.originalData.code;
            },
            position: 'top',
            distance: 5
          },
          labelLayout: labelLayout,
          emphasis: {
            focus: 'self',
            scale: 1.1,
            scaleSize: 5,
            transition: ['itemStyle', 'opacity', 'symbolSize'].map(prop => `${prop}:800`).join(','),
            label: {
              show: false,  // Force hide all labels on hover
              formatter: function(params) {
                return '';  // Return empty string to ensure no label is shown
              }
            },
            itemStyle: {
              shadowBlur: 20,
              shadowColor: 'rgba(0,0,0,0.3)',
              opacity: 1,
              color: undefined  // This will maintain the original color
            }
          }
        }],
      });

      // Add mouse events for hover effects
      this.chart.on('mouseover', { seriesIndex: 0 }, (params) => {
        if (params.data.itemStyle.opacity > 0) {
          this.chart.dispatchAction({
            type: 'highlight',
            seriesIndex: 0,
            dataIndex: params.dataIndex
          });
        }
      });

      this.chart.on('mouseout', { seriesIndex: 0 }, (params) => {
        this.chart.dispatchAction({
          type: 'downplay',
          seriesIndex: 0,
          dataIndex: params.dataIndex
        });
      });

      // Add resize listener
      window.addEventListener('resize', () => {
        this.chart?.resize();
      });
    },
    toggleRegion(region) {
      const index = this.selectedRegions.indexOf(region);
      if (index > -1) {
        this.selectedRegions.splice(index, 1);
      } else {
        this.selectedRegions.push(region);
      }
      this.updateChart();
    },
    determineVisibleLabels(data) {
      // Group points by approximate grid cells to reduce collision checks
      const GRID_SIZE = 50;
      const grid = {};
      
      // Sort data by population (descending)
      const sortedIndices = data.map((_, idx) => idx)
        .sort((a, b) => (data[b].originalData.population || 0) - (data[a].originalData.population || 0));

      const visibleLabels = new Set();
      const LABEL_HEIGHT = 20;
      const LABEL_PADDING = 5;
      const MIN_POPULATION_THRESHOLD = 10000000; // 10 million population threshold

      for (const idx of sortedIndices) {
        const point = data[idx];
        if (point.itemStyle.opacity === 0) continue;

        const [x, y] = point.value;
        const population = point.originalData.population || 0;
        const labelWidth = point.originalData.code.length * 8;

        // Always show labels for countries with large populations
        if (population > MIN_POPULATION_THRESHOLD) {
          visibleLabels.add(idx);
          continue;
        }

        // Grid-based collision detection
        const gridX = Math.floor(x / GRID_SIZE);
        const gridY = Math.floor(y / GRID_SIZE);
        
        // Check surrounding grid cells
        let hasNearbyLabel = false;
        for (let dx = -1; dx <= 1; dx++) {
          for (let dy = -1; dy <= 1; dy++) {
            const key = `${gridX + dx},${gridY + dy}`;
            if (grid[key]) {
              const distance = Math.sqrt(
                Math.pow(x - grid[key].x, 2) + 
                Math.pow(y - grid[key].y, 2)
              );
              if (distance < LABEL_HEIGHT * 1.5) {
                hasNearbyLabel = true;
                break;
              }
            }
          }
          if (hasNearbyLabel) break;
        }

        if (!hasNearbyLabel) {
          visibleLabels.add(idx);
          grid[`${gridX},${gridY}`] = { x, y };
        }
      }

      return visibleLabels;
    },

    updateChart() {
      const visibleData = this.allData.filter(d =>
        this.selectedRegions.includes(d.region)
      );

      const updatedData = visibleData.map(d => ({
        value: [d.logGDP, d.lifeLadder],
        symbolSize: d.population ? Math.sqrt(Math.sqrt(d.population)) / 2 : 10,
        itemStyle: {
          color: this.regionColors[d.region] || '#cccccc',
          opacity: 1, // Always visible for selected regions
          borderColor: '#fff',
          borderWidth: 0.1,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
        label: {
          show: false,
          color: '#2c3e50', // Set a single color for all labels
          position: 'top',
          distance: 5,
          formatter: d.code
        },
        originalData: d,
        z: d.population ? Math.sqrt(d.population) : 1
      }));

      const visibleLabels = this.determineVisibleLabels(updatedData);

      updatedData.forEach((item, idx) => {
        const population = item.originalData.population || 0;
        item.label = {
          ...item.label,
          show: visibleLabels.has(idx),
          fontSize: population > 50000000 ? 14 : 10
        };
      });

      this.chart.setOption({
        animation: true,
        animationDuration: 500,
        animationDurationUpdate: 500,
        animationEasing: 'quadraticInOut',
        animationEasingUpdate: 'quadraticInOut',
        animationThreshold: 2000,
        series: [{
          data: updatedData,
          universalTransition: {
            enabled: true,
            delay: function (idx, count) {
              return idx * 50;
            },
            duration: function (idx, count) {
              return this.selectedRegions.includes(updatedData[idx].originalData.region) ? 1200 : 600;
            }
          },
          emphasis: {
            focus: 'self',
            scale: 1.1,
            scaleSize: 5,
            transition: ['itemStyle', 'opacity', 'symbolSize'].map(prop => `${prop}:800`).join(','),
            label: {
              show: false,  // Force hide all labels on hover
              formatter: function(params) {
                return '';  // Return empty string to ensure no label is shown
              }
            },
            itemStyle: {
              shadowBlur: 20,
              shadowColor: 'rgba(0,0,0,0.3)',
              opacity: 1,
              color: undefined  // This will maintain the original color
            }
          }
        }]
      });
    }
  },
};
</script>

<style>
#scatterplot {
  width: 100%;
  height: 800px;
}

.scatterplot-container {
  display: flex;
  justify-content: flex-start; /* Align content to the left */
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
}

.region-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
  justify-content: center; /* Center content horizontally */
  margin: 10px auto;
}

.region-checkbox {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.region-color-block {
  width: 16px;
  height: 16px;
  cursor: pointer;
  border: 1px solid #2c3e50;
}

.region-checkbox span {
  font-size: 14px;
  padding-left: 4px;
}
</style>

<template>
  <div>
    <div id="scatterplot" style="width: 100%; height: 800px;"></div>
    <div style="margin-top: -20px;">
      <label><strong>Select Regions:</strong></label>
      <div class="region-selector">
        <div v-for="region in availableRegions" :key="region" class="region-checkbox">
          <input
            type="checkbox"
            :value="region"
            v-model="selectedRegions"
            @change="updateChart"
          />
          <span>{{ region }}</span>
        </div>
      </div>
    </div>
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
    };
  },
  mounted() {
    this.loadDataAndRenderChart();
  },
  methods: {
    async loadDataAndRenderChart() {
      try {
        const response = await axios.get('assets/GNH_2023.csv');
        const csvData = response.data;
        const parsedData = this.parseCSV(csvData);

        // Store all data and extract unique regions
        this.allData = parsedData;
        this.availableRegions = [
          ...new Set(parsedData.map(d => d.region).filter(Boolean)),
        ];

        // Initially select all regions
        this.selectedRegions = [...this.availableRegions];

        // Render the chart with initial data
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
    updateChart() {
      const filteredData = this.allData.filter(d =>
        this.selectedRegions.includes(d.region)
      );

      this.renderChart(filteredData);
    },
    renderChart(data) {
      const chart = echarts.init(document.getElementById('scatterplot'));

      const regionColors = {
        Oceania: '#e41a1c',
        Africa: '#377eb8',
        Europe: '#ffcc00',
        Americas: '#4daf4a',
        Asia: '#CC79A7',
      };

      chart.setOption({
        title: {
          text: 'Scatterplot: Life Ladder vs Log GDP per Capita',
          left: 'center',
          top: 'top',
          textStyle: {
            color: '#000',
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        xAxis: {
          name: 'Log GDP per Capita',
          type: 'value',
          min: 7,
          max: 12,
          nameTextStyle: { color: '#000' },
          axisLabel: { color: '#000' },
        },
        yAxis: {
          name: 'Life Ladder',
          type: 'value',
          min: 2,
          nameTextStyle: { color: '#000' },
          axisLabel: { color: '#000' },
        },
        series: [
          {
            type: 'scatter',
            data: data.map(d => ({
              value: [d.logGDP, d.lifeLadder],
              symbolSize: d.population ? Math.sqrt(Math.sqrt(d.population)) / 2 : 10,
              itemStyle: {
                color: regionColors[d.region] || '#cccccc',
              },
              tooltip: {
                // Override default tooltip for each data point
                trigger: 'item',
                formatter: function (params) {
                  return `${d.name} (${d.code})<br>Region: ${d.region}<br>Log GDP: ${params.value[0]}<br>Life Ladder: ${params.value[1]}<br>Population (2021): ${d.population}`;
                },
              },
              z: d.population ? Math.sqrt(d.population) : 1, // Dynamically set z-index based on population
            })),
            label: {
              show: true,
              color: '#000',
              formatter: function (params) {
                return data[params.dataIndex].code;
              },
            },
          },
        ],
        tooltip: {
          trigger: 'item',
          axisPointer: { type: 'shadow' },
          formatter: function (params) {
            const item = data[params.dataIndex];
            return `${item.name} (${item.code})<br>Region: ${item.region}<br>Log GDP: ${params.value[0]}<br>Life Ladder: ${params.value[1]}<br>Population (2021): ${item.population}`;
          },
        },
        legend: {
          data: Object.keys(regionColors),
          textStyle: { color: '#000' },
        },
      });
    }


  },
};
</script>

<style>
#scatterplot {
  margin: auto;
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
</style>

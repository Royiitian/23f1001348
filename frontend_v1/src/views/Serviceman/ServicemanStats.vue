<template>
  <div class="analytics-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <i class="fas fa-history header-icon"></i>
        <div class="title-group">
          <h1 class="dashboard-title">Service History</h1>
          <p class="dashboard-subtitle">Track your performance and service records</p>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <div v-if="loading" class="status-container">
        <div class="loading-spinner"></div>
        <p class="status-message">Analyzing your service history...</p>
      </div>

      <div v-else-if="requests.length === 0" class="status-container empty-state">
        <i class="fas fa-folder-open empty-icon"></i>
        <p class="status-message">No Service History Available</p>
        <p class="status-submessage">Your service records will appear here once you complete services</p>
      </div>

      <div v-else class="analytics-content">
        <div class="analytics-grid">
          <div class="chart-card">
            <div class="chart-header">
              <i class="fas fa-chart-pie chart-icon"></i>
              <h2>Request Status Distribution</h2>
            </div>
            <div class="chart-body">
              <canvas ref="statusChartRef"></canvas>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-header">
              <i class="fas fa-star chart-icon"></i>
              <h2>Rating Distribution</h2>
            </div>
            <div class="chart-body">
              <canvas ref="ratingChartRef"></canvas>
            </div>
          </div>
        </div>

        <div class="data-card">
          <div class="card-header">
            <i class="fas fa-list-alt"></i>
            <h2>Service Records</h2>
          </div>
          
          <div class="table-container">
            <table class="modern-table">
              <thead>
                <tr>
                  <th @click="sortTable('serviceRequest_id')">
                    <div class="th-content">
                      <i class="fas fa-hashtag"></i>
                      Request ID
                      <i :class="getSortClass('serviceRequest_id')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('customer_name')">
                    <div class="th-content">
                      <i class="fas fa-user"></i>
                      Customer
                      <i :class="getSortClass('customer_name')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('service')">
                    <div class="th-content">
                      <i class="fas fa-tools"></i>
                      Service
                      <i :class="getSortClass('service')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('customer_address')">
                    <div class="th-content">
                      <i class="fas fa-map-marker-alt"></i>
                      Location
                      <i :class="getSortClass('customer_address')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('status')">
                    <div class="th-content">
                      <i class="fas fa-info-circle"></i>
                      Status
                      <i :class="getSortClass('status')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('rating')">
                    <div class="th-content">
                      <i class="fas fa-star"></i>
                      Rating
                      <i :class="getSortClass('rating')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('request_begin_date')">
                    <div class="th-content">
                      <i class="fas fa-calendar-alt"></i>
                      Start Date
                      <i :class="getSortClass('request_begin_date')"></i>
                    </div>
                  </th>
                  <th @click="sortTable('request_end_date')">
                    <div class="th-content">
                      <i class="fas fa-flag-checkered"></i>
                      End Date
                      <i :class="getSortClass('request_end_date')"></i>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in sortedRequests" :key="request.serviceRequest_id">
                  <td class="id-cell">#{{ request.serviceRequest_id }}</td>
                  <td>{{ request.customer_name }}</td>
                  <td>{{ request.service }}</td>
                  <td>{{ request.customer_address }}</td>
                  <td>
                    <span class="status-badge" :class="getStatusClass(request.status)">
                      {{ request.status }}
                    </span>
                  </td>
                  <td>
                    <div class="rating-display" v-if="request.rating !== null">
                      <span class="rating-value">{{ request.rating }}</span>
                      <i class="fas fa-star rating-star"></i>
                    </div>
                    <span v-else>N/A</span>
                  </td>
                  <td>{{ formatDate(request.request_begin_date) }}</td>
                  <td>{{ formatDate(request.request_end_date) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const requests = ref([]);
    const loading = ref(true);
    const sortKey = ref('');
    const sortAsc = ref(true);
    const statusChartRef = ref(null);
    const ratingChartRef = ref(null);
    let statusChart = null;
    let ratingChart = null;

    const sortedRequests = computed(() => {
      return [...requests.value].sort((a, b) => {
        const modifier = sortAsc.value ? 1 : -1;
        
        if (sortKey.value === 'request_begin_date' || sortKey.value === 'request_end_date') {
          const dateA = new Date(a[sortKey.value]);
          const dateB = new Date(b[sortKey.value]);
          return (dateA - dateB) * modifier;
        }

        if (a[sortKey.value] < b[sortKey.value]) return -1 * modifier;
        if (a[sortKey.value] > b[sortKey.value]) return 1 * modifier;
        return 0;
      });
    });

    const fetchRequests = async () => {
      loading.value = true;
      try {
        const servicemanId = localStorage.getItem("service_id");
        const token = localStorage.getItem("service_Token");
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/fetchServices/${servicemanId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        requests.value = response.data;
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        loading.value = false;
      }
    };

    const sortTable = (key) => {
      if (sortKey.value === key) {
        sortAsc.value = !sortAsc.value;
      } else {
        sortKey.value = key;
        sortAsc.value = true;
      }
    };

    const getSortClass = (key) => {
      if (sortKey.value === key) {
        return sortAsc.value ? 'asc' : 'desc';
      }
      return '';
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };

    const createCharts = () => {
      createStatusChart();
      createRatingChart();
    };

    const createStatusChart = () => {
      if (statusChart) {
        statusChart.destroy();
      }
      const ctx = statusChartRef.value.getContext('2d');
      const statusCount = {};
      requests.value.forEach(request => {
        statusCount[request.status] = (statusCount[request.status] || 0) + 1;
      });
      
      statusChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: Object.keys(statusCount),
          datasets: [{
            data: Object.values(statusCount),
            backgroundColor: [
              'rgba(75, 192, 192, 0.6)',
              'rgba(255, 99, 132, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(54, 162, 235, 0.6)',
            ],
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: 'black'
              }
            }
          }
        }
      });
    };

    const createRatingChart = () => {
      if (ratingChart) {
        ratingChart.destroy();
      }
      const ctx = ratingChartRef.value.getContext('2d');
      const ratingDistribution = Array(10).fill(0);
      requests.value.forEach(request => {
        if (request.rating !== null) {
          ratingDistribution[request.rating - 1]++;
        }
      });
      
      ratingChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
          datasets: [{
            label: 'Number of Ratings',
            data: ratingDistribution,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Ratings',
                color: 'black'
              },
              ticks: {
                color: 'black'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Rating',
                color: 'black'
              },
              ticks: {
                color: 'black'
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: 'black'
              }
            }
          }
        }
      });
    };

    const getStatusClass = (status) => {
      const statusClasses = {
        'completed': 'status-completed',
        'active': 'status-active',
        'requested': 'status-requested',
        'withdrawn': 'status-withdrawn'
      };
      return statusClasses[status] || 'status-default';
    };

    onMounted(async () => {
      await fetchRequests();
      nextTick(() => {
        if (statusChartRef.value && ratingChartRef.value) {
          createCharts();
        } else {
          console.error('Chart refs not available');
        }
      });
    });

    return {
      requests,
      loading,
      sortedRequests,
      statusChartRef,
      ratingChartRef,
      sortTable,
      getSortClass,
      formatDate,
      getStatusClass,
    };
  }
};
</script>

<style scoped>
.analytics-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
}

.dashboard-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 2rem;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  font-size: 2.5rem;
}

.dashboard-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.dashboard-subtitle {
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.dashboard-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chart-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chart-icon {
  color: #4CAF50;
  font-size: 1.5rem;
}

.chart-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.chart-body {
  padding: 1.5rem;
  height: 300px;
}

.data-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #f8f9fa;
}

.card-header i {
  color: #4CAF50;
  font-size: 1.5rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  background: #f8f9fa;
  padding: 1rem;
  color: #2c3e50;
  font-weight: 600;
  cursor: pointer;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.th-content i:first-child {
  color: #4CAF50;
}

.modern-table td {
  padding: 1rem;
  border-top: 1px solid #eee;
  color: #2c3e50;
}

.id-cell {
  font-family: monospace;
  color: #666;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-completed {
  background: #e8f5e9;
  color: #4CAF50;
}

.status-active {
  background: #e3f2fd;
  color: #1976d2;
}

.status-requested {
  background: #fff3e0;
  color: #f57c00;
}

.status-withdrawn {
  background: #fce4ec;
  color: #e91e63;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating-star {
  color: #ffc107;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.status-container {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 4rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.status-message {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.status-submessage {
  color: #666;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-header {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .modern-table {
    display: block;
    overflow-x: auto;
  }
}
</style>
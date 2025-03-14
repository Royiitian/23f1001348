<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <i class="fas fa-chart-line header-icon"></i>
        <div class="title-group">
          <h1>Analytics Dashboard</h1>
          <p>Monitor platform performance and user activity</p>
        </div>
      </div>
    </header>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Analyzing platform data...</p>
    </div>
    
    <div v-else class="dashboard-content">
      <!-- Stats Cards -->
      <div class="stats-cards">
        <div class="stat-card">
          <i class="fas fa-clipboard-list stat-icon"></i>
          <div class="stat-info">
            <h3>Total Requests</h3>
            <p>{{ requests.length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-check-circle stat-icon"></i>
          <div class="stat-info">
            <h3>Completed Requests</h3>
            <p>{{ requests.filter(r => r.status === 'completed').length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-clock stat-icon"></i>
          <div class="stat-info">
            <h3>Active Requests</h3>
            <p>{{ requests.filter(r => r.status === 'active').length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-users stat-icon"></i>
          <div class="stat-info">
            <h3>Total Users</h3>
            <p>{{ servicemen.length + customers.length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-user-tie stat-icon"></i>
          <div class="stat-info">
            <h3>Total Servicemen</h3>
            <p>{{ servicemen.length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-user stat-icon"></i>
          <div class="stat-info">
            <h3>Total Customers</h3>
            <p>{{ customers.length }}</p>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-container">
        <div class="chart-card">
          <div class="chart-header">
            <i class="fas fa-chart-bar chart-icon"></i>
            <h3>Most Requested Services</h3>
          </div>
          <canvas ref="servicesChartRef"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-header">
            <i class="fas fa-chart-line chart-icon"></i>
            <h3>User Creation Timeline</h3>
          </div>
          <canvas ref="userCreationChartRef"></canvas>
        </div>
      </div>

      <!-- Requests Table -->
      <div class="table-container">
        <div class="table-header">
          <i class="fas fa-list-alt table-icon"></i>
          <h3>All Service Requests</h3>
        </div>
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
              <th @click="sortTable('serviceman_name')">
                <div class="th-content">
                  <i class="fas fa-user-tie"></i>
                  Provider
                  <i :class="getSortClass('serviceman_name')"></i>
                </div>
              </th>
              <th @click="sortTable('service')">
                <div class="th-content">
                  <i class="fas fa-tools"></i>
                  Service
                  <i :class="getSortClass('service')"></i>
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
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in sortedRequests" :key="request.serviceRequest_id">
              <td class="id-cell">#{{ request.serviceRequest_id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.serviceman_name }}</td>
              <td>{{ request.service }}</td>
              <td>
                <span class="status-badge" :class="'status-' + request.status">
                  {{ request.status }}
                </span>
              </td>
              <td>
                <div v-if="request.rating !== null" class="rating-display">
                  {{ request.rating }}
                  <i class="fas fa-star rating-star"></i>
                </div>
                <span v-else>N/A</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Colors } from 'chart.js';
import Chart from 'chart.js/auto';
import { ref, onMounted, nextTick } from 'vue';

export default {
  setup() {
    const requests = ref([]);
    const servicemen = ref([]);
    const customers = ref([]);
    const loading = ref(true);
    const sortKey = ref('');
    const sortAsc = ref(true);
    const servicesChartRef = ref(null);
    const userCreationChartRef = ref(null);

    const fetchAllData = async () => {
      loading.value = true;
      try {
        await Promise.all([
          fetchAllRequests(),
          fetchServicemen(),
          fetchCustomers(),
        ]);
        await nextTick();
        createCharts();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please try again.");
      } finally {
        loading.value = false;
      }
    };

    const fetchAllRequests = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/requests/fetchAllServices",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      requests.value = response.data;
    };

    const fetchServicemen = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/fetch-servicemen",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      servicemen.value = response.data;
    };

    const fetchCustomers = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/fetch-customers",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      customers.value = response.data;
    };

    const createCharts = () => {
      createServicesChart();
      createUserCreationChart();
    };

    const createServicesChart = () => {
      if (!servicesChartRef.value) return;

      const ctx = servicesChartRef.value.getContext('2d');
      const serviceCount = {};
      requests.value.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });
      
      new Chart(ctx, 
    {
  type: 'bar',
  data: {
    labels: Object.keys(serviceCount),
    datasets: [{
      label: 'Number of Requests',
      data: Object.values(serviceCount),
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
          text: 'Number of Requests',
          color: 'black' // Y-axis title color
        },
        ticks: {
          color: 'black' // Y-axis label color
        }
      },
      x: {
        title: {
          display: true,
          text: 'Service Type',
          color: 'black' // X-axis title color
        },
        ticks: {
          color: 'black' // X-axis label color
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: 'black' // Legend text color
        }
      }
    }
  }
});

    };

    const createUserCreationChart = () => {
  if (!userCreationChartRef.value) return;

  const ctx = userCreationChartRef.value.getContext('2d');
  const customerData = processUserCreationData(customers.value);
  const servicemanData = processUserCreationData(servicemen.value);
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: generateDateLabels(),
      datasets: [
        {
          label: 'Customers',
          data: customerData,
          borderColor: 'rgba(75, 192, 192, 1)',
          fill: false
        },
        {
          label: 'Servicemen',
          data: servicemanData,
          borderColor: 'rgba(255, 99, 132, 1)',
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Users',
            color: 'black' // Y-axis title color
          },
          ticks: {
            color: 'black' // Y-axis label color
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date',
            color: 'black' // X-axis title color
          },
          ticks: {
            color: 'black' // X-axis label color
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: 'black' // Legend text color
          }
        }
      }
    }
  });
};
    const processUserCreationData = (users) => {
      const dateCounts = {};
      users.forEach(user => {
        const date = new Date(user.date_created).toISOString().split('T')[0];
        dateCounts[date] = (dateCounts[date] || 0) + 1;
      });
      return generateDateLabels().map(date => dateCounts[date] || 0);
    };

    const generateDateLabels = () => {
      const allUsers = [...customers.value, ...servicemen.value];
      const startDate = new Date(Math.min(...allUsers.map(u => new Date(u.date_created))));
      const endDate = new Date();
      const dateLabels = [];
      for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        dateLabels.push(d.toISOString().split('T')[0]);
      }
      return dateLabels;
    };

    onMounted(() => {
      fetchAllData();
    });

    return {
      requests,
      servicemen,
      customers,
      loading,
      sortKey,
      sortAsc,
      servicesChartRef,
      userCreationChartRef,
      fetchAllData,
      createCharts,
    };
  },
  computed: {
    sortedRequests() {
      return this.requests.slice().sort((a, b) => {
        const modifier = this.sortAsc ? 1 : -1;
        if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
        if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
        return 0;
      });
    },
    totalRequests() {
      return this.requests.length;
    },
    completedRequests() {
      return this.requests.filter(r => r.status === 'completed').length;
    },
    activeRequests() {
      return this.requests.filter(r => r.status === 'active').length;
    },
    totalUsers() {
      return this.servicemen.length + this.customers.length;
    },
    totalServicemen() {
      return this.servicemen.length;
    },
    totalCustomers() {
      return this.customers.length;
    },
  },
  methods: {
    async fetchAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.fetchAllRequests(),
          this.fetchServicemen(),
          this.fetchCustomers(),
        ]);
        this.createCharts();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please try again.");
      } finally {
        this.loading = false;
      }
    },
    async fetchAllRequests() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/requests/listAllServices",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.requests = response.data;
    },
    async fetchServicemen() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/fetch-servicemen",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.servicemen = response.data;
    },
    async fetchCustomers() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/fetch-customers",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.customers = response.data;
    },
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },
    getSortClass(key) {
      if (this.sortKey === key) {
        return this.sortAsc ? 'asc' : 'desc';
      }
      return '';
    },
    createCharts() {
      this.createServicesChart();
      this.createUserCreationChart();
    },
    createServicesChart() {
      const ctx = this.$refs.servicesChart.getContext('2d');
      const serviceCount = {};
      this.requests.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });
      
      this.servicesChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: Object.keys(serviceCount),
    datasets: [{
      label: 'Number of Requests',
      data: Object.values(serviceCount),
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
          text: 'Number of Requests',
          color: 'black' // Y-axis title color
        },
        ticks: {
          color: 'black' // Y-axis label color
        }
      },
      x: {
        title: {
          display: true,
          text: 'Service Type',
          color: 'black' // X-axis title color
        },
        ticks: {
          color: 'black' // X-axis label color
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: 'black' // Legend text color
        }
      }
    }
  }
});
    },
    createUserCreationChart() {
      const ctx = this.$refs.userCreationChart.getContext('2d');
      const customerData = this.processUserCreationData(this.customers);
      const servicemanData = this.processUserCreationData(this.servicemen);
      
      this.userCreationChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.generateDateLabels(),
          datasets: [
            {
              label: 'Customers',
              data: customerData,
              borderColor: 'rgba(75, 192, 192, 1)',
              fill: false
            },
            {
              label: 'Servicemen',
              data: servicemanData,
              borderColor: 'rgba(255, 99, 132, 1)',
              fill: false
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Users'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      });
    },
    processUserCreationData(users) {
      const dateCounts = {};
      users.forEach(user => {
        const date = new Date(user.date_created).toISOString().split('T')[0];
        dateCounts[date] = (dateCounts[date] || 0) + 1;
      });
      return this.generateDateLabels().map(date => dateCounts[date] || 0);
    },
    generateDateLabels() {
      const startDate = new Date(Math.min(...this.customers.concat(this.servicemen).map(u => new Date(u.date_created))));
      const endDate = new Date();
      const dateLabels = [];
      for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        dateLabels.push(d.toISOString().split('T')[0]);
      }
      return dateLabels;
    }
  },
  created() {
    this.fetchAllData();
  },
};
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
  padding: 2rem;
}

.dashboard-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 2rem;
  border-radius: 12px;
  color: white;
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  font-size: 2.5rem;
}

.title-group h1 {
  margin: 0;
  font-size: 2rem;
}

.title-group p {
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.loading {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
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

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 2rem;
  color: #4CAF50;
}

.stat-info h3 {
  margin: 0;
  font-size: 0.875rem;
  color: #666;
}

.stat-info p {
  margin: 0.25rem 0 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.chart-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.chart-icon {
  color: #4CAF50;
}

.chart-header h3 {
  margin: 0;
  color: #2c3e50;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.table-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid #eee;
}

.table-icon {
  color: #4CAF50;
  font-size: 1.25rem;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 1rem;
  color: #2c3e50;
}

.th-content i:first-child {
  color: #4CAF50;
}

.modern-table td {
  padding: 1rem;
  border-top: 1px solid #eee;
  color: #4a5568;
}

.id-cell {
  font-family: monospace;
  color: #666;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
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

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating-star {
  color: #ffc107;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .modern-table {
    font-size: 0.875rem;
  }
}
</style>
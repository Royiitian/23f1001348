<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <i class="fas fa-clipboard-check header-icon"></i>
        <div class="title-group">
          <h1 class="dashboard-title">Service Requests</h1>
          <p class="dashboard-subtitle">Manage incoming service requests</p>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <div v-if="loading" class="status-container">
        <div class="loading-spinner"></div>
        <p class="status-message">Loading your requests...</p>
      </div>

      <div v-else-if="requests.length === 0" class="status-container empty-state">
        <i class="fas fa-inbox empty-icon"></i>
        <p class="status-message">No Pending Requests</p>
        <p class="status-submessage">New service requests will appear here</p>
      </div>

      <div v-else class="requests-wrapper">
        <div class="table-container">
          <table class="modern-table">
            <thead>
              <tr>
                <th>
                  <div class="th-content">
                    <i class="fas fa-hashtag"></i>
                    Request ID
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-user"></i>
                    Customer
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-tools"></i>
                    Service
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-map-marker-alt"></i>
                    Location
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-info-circle"></i>
                    Status
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-calendar-alt"></i>
                    Request Date
                  </div>
                </th>
                <th>
                  <div class="th-content">
                    <i class="fas fa-cogs"></i>
                    Actions
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.serviceRequest_id">
                <td class="id-cell">#{{ request.serviceRequest_id }}</td>
                <td>{{ request.customer_name }}</td>
                <td>{{ request.service }}</td>
                <td>{{ request.customer_address }}</td>
                <td>
                  <span class="status-badge">{{ request.status }}</span>
                </td>
                <td>{{ formatDate(request.request_begin_date) }}</td>
                <td class="actions-cell">
                  <button 
                    @click="updateRequest(request.serviceRequest_id, 'active')" 
                    class="action-button accept-btn"
                  >
                    <i class="fas fa-check"></i>
                    Accept
                  </button>
                  <button 
                    @click="updateRequest(request.serviceRequest_id, 'rejected')" 
                    class="action-button reject-btn"
                  >
                    <i class="fas fa-times"></i>
                    Reject
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      requests: [],
      loading: true,
    };
  },
  methods: {
    async fetchRequests() {
      this.loading = true;
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
        this.requests = response.data.filter(request => request.status === "requested");
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },
    async updateRequest(serviceRequestId, status) {
      try {
        const token = localStorage.getItem("service_Token");
        const response = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/requests/modifyServiceRequest",
          data: {
            serviceRequest_id: serviceRequestId,
            status: status,
          },
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token}`,
          },
          withCredentials: false,
        });
        alert(response.data.message);
        await this.fetchRequests();
      } catch (error) {
        console.error("Error updating service request:", error);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
          console.error("Response headers:", error.response.headers);
        } else if (error.request) {
          console.error("No response received:", error.request);
        } else {
          console.error("Error setting up request:", error.message);
        }
        alert("Failed to update service request. Please check the console for more details.");
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },
  },
  created() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.dashboard-container {
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

.status-container {
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

.requests-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
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
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.th-content i {
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
  background: #fff3e0;
  color: #f57c00;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 50px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.accept-btn {
  background: #4CAF50;
  color: white;
}

.reject-btn {
  background: #f44336;
  color: white;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
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

  .actions-cell {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
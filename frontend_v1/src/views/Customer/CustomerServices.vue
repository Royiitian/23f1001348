<!-- CHANGED -->
<template>
  <div class="service-dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <i class="fas fa-clipboard-list header-icon"></i>
        <div class="title-group">
          <h1 class="dashboard-title">Service Requests</h1>
          <p class="dashboard-subtitle">Track and manage your service requests</p>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <div v-if="loading" class="status-container">
        <div class="loading-spinner"></div>
        <p class="status-message">Fetching your requests...</p>
      </div>

      <div v-else-if="requests.length === 0" class="status-container empty-state">
        <i class="fas fa-inbox empty-icon"></i>
        <p class="status-message">No active service requests found</p>
        <p class="status-submessage">Your pending requests will appear here</p>
      </div>

      <div v-else class="requests-wrapper">
        <div class="table-container">
          <table class="modern-table">
            <thead>
              <tr>
                <th>
                  <i class="fas fa-hashtag"></i>
                  Request ID
                </th>
                <th>
                  <i class="fas fa-user-tie"></i>
                  Provider
                </th>
                <th>
                  <i class="fas fa-id-card"></i>
                  Provider ID
                </th>
                <th>
                  <i class="fas fa-tools"></i>
                  Service
                </th>
                <th>
                  <i class="fas fa-info-circle"></i>
                  Status
                </th>
                <th>
                  <i class="fas fa-calendar-alt"></i>
                  Date
                </th>
                <th>
                  <i class="fas fa-cogs"></i>
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.serviceRequest_id">
                <td class="request-id">#{{ request.serviceRequest_id }}</td>
                <td>{{ request.serviceman_name }}</td>
                <td>{{ request.serviceman_id }}</td>
                <td>{{ request.service }}</td>
                <td>
                  <span class="status-badge" :class="getStatusClass(request.status)">
                    {{ request.status }}
                  </span>
                </td>
                <td>{{ formatDate(request.request_begin_date) }}</td>
                <td class="actions-cell">
                  <button 
                    @click="withdrawRequest(request.serviceRequest_id)" 
                    class="action-button withdraw-btn"
                    :disabled="request.status === 'active'"
                    :title="request.status === 'active' ? 'Cannot withdraw active request' : 'Withdraw request'"
                  >
                    <i class="fas fa-undo"></i>
                    <span>Withdraw</span>
                  </button>
                  <button 
                    @click="openCompletionModal(request.serviceRequest_id)" 
                    class="action-button complete-btn"
                    :disabled="request.status === 'requested'"
                    :title="request.status === 'requested' ? 'Request not yet active' : 'Mark as completed'"
                  >
                    <i class="fas fa-check-circle"></i>
                    <span>Complete</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Modern Rating Modal -->
    <div v-if="showCompletionModal" class="modal-overlay" @click.self="closeCompletionModal">
      <div class="modern-modal">
        <div class="modal-header">
          <h3>Rate Your Experience</h3>
          <button class="close-modal" @click="closeCompletionModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <p class="rating-instruction">How would you rate the service? (1-10)</p>
          <div class="rating-input-group">
            <input 
              v-model.number="rating" 
              type="range" 
              min="1" 
              max="10" 
              class="rating-slider"
              id="rating-input"
            >
            <div class="rating-value">{{ rating }}</div>
          </div>
          <div class="rating-labels">
            <span>Poor</span>
            <span>Excellent</span>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeCompletionModal" class="modal-button cancel-btn">
            <i class="fas fa-times"></i> Cancel
          </button>
          <button @click="submitCompletion" class="modal-button submit-btn">
            <i class="fas fa-paper-plane"></i> Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      requests: [],
      loading: true,
      showCompletionModal: false,
      selectedRequestId: null,
      rating: 5,
    };
  },
  methods: {
    async fetchRequests() {
      this.loading = true;
      try {
        const customerId = localStorage.getItem("cust_id");
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/fetchCustomerServices/${customerId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.requests = response.data.filter(request => 
          request.status === "open" || request.status === "requested" || request.status === "active"
        );
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },
    async updateRequest(serviceRequestId, status, rating = null) {
      try {
        const token = localStorage.getItem("cust_Token");
        const data = {
          serviceRequest_id: serviceRequestId,
          status: status,
        };
        if (rating !== null) {
          data.rating = rating;
        }
        const response = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/requests/modifyServiceRequest",
          data: data,
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token}`,
          },
        });
        alert(response.data.message);
        await this.fetchRequests();
      } catch (error) {
        console.error("Error updating service request:", error);
        alert("Failed to update service request. Please try again.");
      }
    },
    withdrawRequest(serviceRequestId) {
      if (confirm("Are you sure you want to withdraw this request?")) {
        this.updateRequest(serviceRequestId, "withdrawn");
      }
    },
    openCompletionModal(serviceRequestId) {
      this.selectedRequestId = serviceRequestId;
      this.showCompletionModal = true;
    },
    closeCompletionModal() {
      this.showCompletionModal = false;
      this.selectedRequestId = null;
      this.rating = 5;
    },
    submitCompletion() {
      if (this.rating < 1 || this.rating > 10) {
        alert("Please enter a rating between 1 and 10.");
        return;
      }
      this.updateRequest(this.selectedRequestId, "completed", this.rating);
      this.closeCompletionModal();
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
    getStatusClass(status) {
      const statusClasses = {
        'requested': 'status-requested',
        'active': 'status-active',
        'open': 'status-open'
      };
      return statusClasses[status] || 'status-default';
    },
  },
  created() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.service-dashboard {
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
  background: #f5f5f5;
  padding: 1rem;
  text-align: left;
  color: #2c3e50;
  font-weight: 600;
}

.modern-table th i {
  margin-right: 0.5rem;
  color: #4CAF50;
}

.modern-table td {
  padding: 1rem;
  border-top: 1px solid #eee;
  color: #2c3e50;
}

.request-id {
  font-family: monospace;
  color: #666;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-requested {
  background: #fff3e0;
  color: #f57c00;
}

.status-active {
  background: #e8f5e9;
  color: #4CAF50;
}

.status-open {
  background: #e3f2fd;
  color: #1976d2;
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

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.withdraw-btn {
  background: #ff9800;
  color: white;
}

.complete-btn {
  background: #4CAF50;
  color: white;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modern-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-modal {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
}

.modal-body {
  padding: 2rem;
}

.rating-instruction {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  text-align: center;
}

.rating-input-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.rating-slider {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
}

.rating-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #4CAF50;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.3s;
}

.rating-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #4CAF50;
  min-width: 2.5rem;
  text-align: center;
}

.rating-labels {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.9rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.modal-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: #e0e0e0;
  color: #333;
}

.submit-btn {
  background: #4CAF50;
  color: white;
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
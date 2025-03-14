<template>
  <div class="approval-container">
    <header class="approval-header">
      <div class="header-content">
        <i class="fas fa-user-shield header-icon"></i>
        <div class="title-group">
          <h1>User Management</h1>
          <p>Manage and approve platform users</p>
        </div>
      </div>
    </header>

    <div class="tab-container">
      <button 
        @click="activeTable = 'servicemen'" 
        :class="['tab-button', { active: activeTable === 'servicemen' }]"
      >
        <i class="fas fa-user-tie"></i>
        Service Providers
      </button>
      <button 
        @click="activeTable = 'customers'" 
        :class="['tab-button', { active: activeTable === 'customers' }]"
      >
        <i class="fas fa-users"></i>
        Customers
      </button>
    </div>

    <div class="search-container">
      <div class="search-box">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          :placeholder="activeTable === 'servicemen' ? 'Search service providers...' : 'Search customers...'"
          class="search-input"
        >
      </div>
      <div class="filter-options">
        <select v-model="searchField" class="filter-select">
          <option value="all">All Fields</option>
          <option value="user_id">ID</option>
          <option value="full_name">Name</option>
          <template v-if="activeTable === 'servicemen'">
            <option value="service">Service</option>
            <option value="pin_code">Pin Code</option>
          </template>
          <template v-else>
            <option value="mail">Email</option>
            <option value="mobile">Mobile</option>
            <option value="pin_code">Pin Code</option>
          </template>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr v-if="activeTable === 'servicemen'">
            <th @click="sortTable('user_id')">
              <div class="th-content">
                <i class="fas fa-hashtag"></i>
                ID
                <i :class="getSortClass('user_id')"></i>
              </div>
            </th>
            <th @click="sortTable('full_name')">
              <div class="th-content">
                <i class="fas fa-user"></i>
                Name
                <i :class="getSortClass('full_name')"></i>
              </div>
            </th>
            <th @click="sortTable('service')">
              <div class="th-content">
                <i class="fas fa-tools"></i>
                Service
                <i :class="getSortClass('service')"></i>
              </div>
            </th>
            <th @click="sortTable('Rating')">
              <div class="th-content">
                <i class="fas fa-star"></i>
                Rating
                <i :class="getSortClass('Rating')"></i>
              </div>
            </th>
            <th @click="sortTable('experience')">
              <div class="th-content">
                <i class="fas fa-briefcase"></i>
                Experience
                <i :class="getSortClass('experience')"></i>
              </div>
            </th>
            <th @click="sortTable('pin_code')">
              <div class="th-content">
                <i class="fas fa-map-marker-alt"></i>
                Pin Code
                <i :class="getSortClass('pin_code')"></i>
              </div>
            </th>
            <th>
              <div class="th-content">
                <i class="fas fa-check-circle"></i>
                Status
              </div>
            </th>
          </tr>
          <tr v-else>
            <th @click="sortTable('user_id')">
              <div class="th-content">
                <i class="fas fa-hashtag"></i>
                ID
                <i :class="getSortClass('user_id')"></i>
              </div>
            </th>
            <th @click="sortTable('full_name')">
              <div class="th-content">
                <i class="fas fa-user"></i>
                Name
                <i :class="getSortClass('full_name')"></i>
              </div>
            </th>
            <th @click="sortTable('mail')">
              <div class="th-content">
                <i class="fas fa-envelope"></i>
                Email
                <i :class="getSortClass('mail')"></i>
              </div>
            </th>
            <th @click="sortTable('mobile')">
              <div class="th-content">
                <i class="fas fa-phone"></i>
                Mobile
                <i :class="getSortClass('mobile')"></i>
              </div>
            </th>
            <th @click="sortTable('pin_code')">
              <div class="th-content">
                <i class="fas fa-map-marker-alt"></i>
                Pin Code
                <i :class="getSortClass('pin_code')"></i>
              </div>
            </th>
            <th>
              <div class="th-content">
                <i class="fas fa-check-circle"></i>
                Status
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in sortedUsers" :key="user.user_id">
            <td class="id-cell">#{{ user.user_id }}</td>
            <td>
              <a 
                v-if="activeTable === 'servicemen'" 
                :href="getPdfUrl(user.user_id)" 
                target="_blank"
                class="portfolio-link"
              >
                <i class="fas fa-file-pdf"></i>
                {{ user.full_name }}
              </a>
              <span v-else>{{ user.full_name }}</span>
            </td>
            <td v-if="activeTable === 'servicemen'">{{ user.service }}</td>
            <td v-if="activeTable === 'servicemen'" class="rating-cell">
              <span v-if="user.Rating !== null">
                {{ user.Rating }}
                <i class="fas fa-star rating-star"></i>
              </span>
              <span v-else>N/A</span>
            </td>
            <td v-if="activeTable === 'servicemen'">{{ user.experience }} years</td>
            <td v-if="activeTable === 'customers'">{{ user.mail }}</td>
            <td v-if="activeTable === 'customers'">{{ user.mobile }}</td>
            <td>{{ user.pin_code }}</td>
            <td>
              <div class="status-cell">
                <span :class="['status-badge', user.approval ? 'approved' : 'pending']">
                  {{ user.approval ? 'Approved' : 'Pending' }}
                </span>
                <button 
                  @click="updateApproval(user)" 
                  :class="['action-button', user.approval ? 'revoke-btn' : 'approve-btn']"
                >
                  <i :class="user.approval ? 'fas fa-times' : 'fas fa-check'"></i>
                  {{ user.approval ? 'Revoke' : 'Approve' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      servicemen: [],
      customers: [],
      activeTable: 'servicemen',
      sortKey: '',
      sortAsc: true,
      searchQuery: '',
      searchField: 'all',
    };
  },
  computed: {
    sortedUsers() {
      const users = this.activeTable === 'servicemen' ? this.servicemen : this.customers;
      
      // First filter the users based on search
      let filteredUsers = users;
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filteredUsers = users.filter(user => {
          if (this.searchField === 'all') {
            return Object.values(user).some(value => 
              String(value).toLowerCase().includes(query)
            );
          } else {
            return String(user[this.searchField]).toLowerCase().includes(query);
          }
        });
      }

      // Then sort the filtered results
      return filteredUsers.sort((a, b) => {
        if (!this.sortKey) return 0;
        const modifier = this.sortAsc ? 1 : -1;
        if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
        if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
        return 0;
      });
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("admin_Token");
        const servicemanResponse = await axios.get(
          "http://127.0.0.1:5000/users/fetch-servicemen",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.servicemen = servicemanResponse.data;

        const customerResponse = await axios.get(
          "http://127.0.0.1:5000/users/fetch-customers",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.customers = customerResponse.data;
      } catch (error) {
        console.error("Error fetching users:", error);
        alert("Failed to fetch user data. Please try again.");
      }
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
    getPdfUrl(servicemanId) {
      return `http://127.0.0.1:5000/users/fetch-portfolio/${servicemanId}`;
    },
    async updateApproval(user) {
      try {
        const token = localStorage.getItem("admin_Token");
        const response = await axios.put(
          `http://127.0.0.1:5000/users/update-status/${user.user_id}`,
          { approval: (!user.approval).toString() },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`
            },
          }
        );
        if (response.status === 200) {
          await this.fetchUsers();  // Reload the table
          alert("Approval status updated successfully");
        }
      } catch (error) {
        console.error("Error updating approval status:", error);
        alert("Failed to update approval status. Please try again.");
      }
    }
  },
  created() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.approval-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
  padding: 2rem;
}

.approval-header {
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

.tab-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
  color: #666;
}

.tab-button i {
  font-size: 1.2rem;
}

.tab-button.active {
  background: #4CAF50;
  color: white;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  color: #2c3e50;
  cursor: pointer;
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

.portfolio-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4CAF50;
  text-decoration: none;
  transition: color 0.3s;
}

.portfolio-link:hover {
  color: #45a049;
}

.rating-cell {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating-star {
  color: #ffc107;
}

.status-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 500;
}

.approved {
  background: #e8f5e9;
  color: #4CAF50;
}

.pending {
  background: #fff3e0;
  color: #f57c00;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.approve-btn {
  background: #4CAF50;
  color: white;
}

.revoke-btn {
  background: #f44336;
  color: white;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  gap: 1rem;
  margin-left: auto;
}

.search-box {
  position: relative;
  min-width: 300px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 2.5rem;
  border: none;
  border-radius: 8px;
  background: white;
  font-size: 0.875rem;
  color: #2c3e50;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.filter-options {
  display: flex;
  align-items: center;
}

.filter-select {
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background: white;
  color: #2c3e50;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

@media (max-width: 768px) {
  .approval-container {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .tab-container {
    flex-direction: column;
  }

  .modern-table {
    font-size: 0.875rem;
  }

  .status-cell {
    flex-direction: column;
    gap: 0.5rem;
  }

  .action-button {
    width: 100%;
    justify-content: center;
  }

  .search-container {
    width: 100%;
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-box {
    min-width: 100%;
  }

  .filter-select {
    width: 100%;
  }
}
</style>
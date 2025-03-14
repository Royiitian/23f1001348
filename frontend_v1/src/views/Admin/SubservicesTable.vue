<template>
  <div class="subservices-container">
    <div v-if="!subservices.length" class="empty-state">
      <i class="fas fa-list-ul empty-icon"></i>
      <p>No subservices found for this service</p>
    </div>
    
    <div v-else class="table-wrapper">
      <table class="modern-table">
        <thead>
          <tr>
            <th>
              <div class="th-content">
                <i class="fas fa-hashtag"></i>
                ID
              </div>
            </th>
            <th>
              <div class="th-content">
                <i class="fas fa-tag"></i>
                Name
              </div>
            </th>
            <th>
              <div class="th-content">
                <i class="fas fa-dollar-sign"></i>
                Base Rate
              </div>
            </th>
            <th>
              <div class="th-content">
                <i class="fas fa-cog"></i>
                Actions
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subservice in filteredSubservices" :key="subservice.subservice_id">
            <td class="id-cell">#{{ subservice.subservice_id }}</td>
            <td>{{ subservice.subservice_name }}</td>
            <td class="rate-cell">₹{{ subservice.base_rate }}</td>
            <td>
              <button 
                @click="$emit('edit-subservice', subservice)" 
                class="action-button edit-btn"
              >
                <i class="fas fa-edit"></i>
                <span>Edit</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubservicesTable',
  props: {
    subservices: {
      type: Array,
      required: true
    },
    serviceName: {
      type: String,
      required: true
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  computed: {
    filteredSubservices() {
      if (!this.searchQuery) return this.subservices;
      const query = this.searchQuery.toLowerCase();
      return this.subservices.filter(subservice =>
        subservice.subservice_name.toLowerCase().includes(query)
      );
    }
  }
};
</script>

<style scoped>
.subservices-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-state .empty-icon {
  font-size: 3rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.table-wrapper {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  white-space: nowrap;
}

.modern-table thead {
  background: #f8f9fa;
}

.modern-table th {
  padding: 1rem;
  font-weight: 600;
  color: #2c3e50;
  text-align: left;
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
  color: #4a5568;
}

.id-cell {
  font-family: monospace;
  color: #666;
}

.rate-cell {
  font-family: monospace;
  color: #2c3e50;
  font-weight: 500;
}

.action-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: #2196F3;
  color: white;
}

.edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: #1e88e5;
}

/* Custom scrollbar */
.table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #43a047;
}

/* Hover effect on table rows */
.modern-table tbody tr {
  transition: background-color 0.3s;
}

.modern-table tbody tr:hover {
  background-color: #f8faf8;
}

@media (max-width: 768px) {
  .modern-table {
    font-size: 0.875rem;
  }

  .modern-table th,
  .modern-table td {
    padding: 0.75rem;
  }

  .action-button {
    padding: 0.4rem 0.8rem;
  }
}
</style>
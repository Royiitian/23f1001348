<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-title">
          <i class="fas fa-cogs header-icon"></i>
          <div class="title-group">
            <h1>Services Management</h1>
            <p>Manage your platform's services and subservices</p>
          </div>
        </div>
        
        <div class="header-actions">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              type="text" 
              class="search-input" 
              placeholder="Search services or subservices..." 
              v-model="searchQuery"
            >
          </div>
          
          <button class="create-btn" @click="showCreateServiceModal = true">
            <i class="fas fa-plus-circle"></i>
            <span>Create Service</span>
          </button>
        </div>
      </div>
    </header>

    <main class="dashboard-content">
      <div v-if="loading" class="status-container">
        <div class="loading-spinner"></div>
        <p class="status-message">Loading services...</p>
      </div>

      <div v-else-if="processedServices.length === 0" class="status-container empty-state">
        <i class="fas fa-box-open empty-icon"></i>
        <p class="status-message">No Services Available</p>
        <p class="status-submessage">Create your first service to get started</p>
      </div>

      <div v-else>
        <div class="services-wrapper">
          <div class="services-grid">
            <div v-for="service in processedServices" :key="service.service_id" class="service-card">
              <div class="service-header">
                <h3>{{ service.service_info.service_name }}</h3>
                <span class="service-date">Created: {{ service.service_info.date_created }}</span>
              </div>
              
              <p class="service-description">{{ service.service_info.service_desc }}</p>
              
              <div class="action-buttons">
                <button @click="showAddSubserviceModal(service)" class="action-btn add-btn">
                  <i class="fas fa-plus-circle"></i>
                  <span>Add Subservice</span>
                </button>
                
                <button @click="showEditServiceModal(service)" class="action-btn edit-btn">
                  <i class="fas fa-edit"></i>
                  <span>Edit Service</span>
                </button>
                
                <button @click="showDeleteSubserviceModal(service)" class="action-btn remove-btn">
                  <i class="fas fa-minus-circle"></i>
                  <span>Remove Subservice</span>
                </button>
                
                <button @click="toggleSubservices(service)" class="action-btn view-btn">
                  <i class="fas fa-eye"></i>
                  <span>View Subservices</span>
                </button>
                
                <button @click="confirmDeleteService(service)" class="action-btn delete-btn">
                  <i class="fas fa-trash-alt"></i>
                  <span>Delete Service</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="subservices-wrapper" v-if="selectedService">
          <div class="section-header">
            <i class="fas fa-list-ul section-icon"></i>
            <h2>Subservices for {{ selectedService.service_info.service_name }}</h2>
          </div>
          <SubservicesTable
            :subservices="filteredSubservices"
            :serviceName="selectedService.service_info.service_name"
            :searchQuery="searchQuery"
            @edit-subservice="showEditSubserviceModal"
          />
        </div>
      </div>
    </main>

    <!-- Create Service Modal -->
    <div v-if="showCreateServiceModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Service</h5>
            <button type="button" class="close" @click="closeCreateServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitCreateServiceForm">
              <div class="form-group">
                <label for="serviceName">Service Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="serviceName"
                  v-model="createServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="serviceDescription">Service Description</label>
                <textarea
                  class="form-control"
                  id="serviceDescription"
                  v-model="createServiceForm.service_description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeCreateServiceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Subservice Modal -->
    <div v-if="showAddSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Subservice</h5>
            <button type="button" class="close" @click="closeAddSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitAddSubserviceForm">
              <div class="form-group">
                <label for="subserviceName">Subservice Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="subserviceName"
                  v-model="addSubserviceForm.subservice_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="baseRate">Base Rate</label>
                <input
                  type="number"
                  class="form-control"
                  id="baseRate"
                  v-model.number="addSubserviceForm.base_rate"
                  required
                  min="0"
                  step="1"
                />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeAddSubserviceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Subservice Modal -->
    <div v-if="showDeleteSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Subservice</h5>
            <button type="button" class="close" @click="closeDeleteSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitDeleteSubserviceForm">
              <div class="form-group">
                <label for="subserviceSelect">Select Subservice to Delete</label>
                <select
                  class="form-control"
                  id="subserviceSelect"
                  v-model="deleteSubserviceForm.subservice_name"
                  required
                >
                  <option v-for="subservice in selectedService.subservices" :key="subservice.subservice_id" :value="subservice.subservice_name">
                    {{ subservice.subservice_name }}
                  </option>
                </select>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeDeleteSubserviceModal">Cancel</button>
                <button type="submit" class="btn btn-danger">Delete</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Service Confirmation Modal -->
    <div v-if="showDeleteServiceModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete Service</h5>
            <button type="button" class="close" @click="closeDeleteServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete "{{ selectedService.service_info.service_name }}"?</p>
            <p>This will also delete all associated subservices.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteServiceModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteService">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Service Modal -->
    <div v-if="showEditServiceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Service</h5>
            <button type="button" class="close" @click="closeEditServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditServiceForm">
              <div class="form-group">
                <label for="editServiceName">Service Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editServiceName"
                  v-model="editServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="editServiceDescription">Service Description</label>
                <textarea
                  class="form-control"
                  id="editServiceDescription"
                  v-model="editServiceForm.service_description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditServiceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Subservice Modal -->
    <div v-if="showEditSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Subservice</h5>
            <button type="button" class="close" @click="closeEditSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditSubserviceForm">
              <div class="form-group">
                <label for="editSubserviceName">Subservice Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editSubserviceName"
                  v-model="editSubserviceForm.subservice_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="editBaseRate">Base Rate</label>
                <input
                  type="number"
                  class="form-control"
                  id="editBaseRate"
                  v-model.number="editSubserviceForm.base_rate"
                  required
                  min="0"
                  step="1"
                />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditSubserviceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SubservicesTable from './SubservicesTable.vue';

export default {
  components: {
    SubservicesTable
  },
  data() {
    return {
      rawServices: [],
      loading: true,
      showCreateServiceModal: false,
      showAddSubserviceModalbool: false,
      showDeleteSubserviceModalbool: false,
      showDeleteServiceModal: false,
      selectedService: null,
      searchQuery: '',
      selectedService: null,
      showEditServiceModalbool: false,
      showEditSubserviceModalbool: false,

      createServiceForm: {
        service_name: "",
        service_description: "",
      },
      addSubserviceForm: {
        subservice_name: "",
        base_rate: null,
      },
      deleteSubserviceForm: {
        subservice_name: "",
      },
      editServiceForm: {
        service_actual_id: null,
        service_name: "",
        service_description: "",
      },
      editSubserviceForm: {
        subservice_id: null,
        subservice_name: "",
        subservice_previous_name: "",
        base_rate: null,
      },
    };
  },
  computed: {
    processedServices() {
      return this.rawServices.map(service => ({
        ...service,
        showSubservices: false
      })).filter(service => {
        const searchLower = this.searchQuery.toLowerCase();
        return service.service_info.service_name.toLowerCase().includes(searchLower) ||
               service.service_info.service_desc.toLowerCase().includes(searchLower) ||
               service.subservices.some(subservice => 
                 subservice.subservice_name.toLowerCase().includes(searchLower)
               );
      });
    },
    filteredSubservices() {
      if (!this.selectedService) return [];
      const searchLower = this.searchQuery.toLowerCase();
      return this.selectedService.subservices.filter(subservice =>
        subservice.subservice_name.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    toggleSubservices(service) {
      service.showSubservices = !service.showSubservices;
      this.selectedService = service.showSubservices ? service : null;
    },
    async fetchServices() {
      this.loading = true;
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.get('http://127.0.0.1:5000/services/fetchAllServices', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
          },
        });
        if (Array.isArray(response.data)) {
          this.rawServices = response.data;
        } else {
          console.error('Unexpected data format:', response.data);
          this.rawServices = [];
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        this.rawServices = [];
      } finally {
        this.loading = false;
      }
    },
    showAddSubserviceModal(service) {
      this.selectedService = service;
      this.showAddSubserviceModalbool = true;
    },
    showDeleteSubserviceModal(service) {
      this.selectedService = service;
      this.showDeleteSubserviceModalbool = true;
    },
    confirmDeleteService(service) {
      this.selectedService = service;
      this.showDeleteServiceModal = true;
    },
    closeCreateServiceModal() {
      this.showCreateServiceModal = false;
      this.createServiceForm = { service_name: "", service_description: "" };
    },
    closeAddSubserviceModal() {
      this.showAddSubserviceModalbool = false;
      this.addSubserviceForm = { subservice_name: "", base_rate: null };
    },
    closeDeleteSubserviceModal() {
      this.showDeleteSubserviceModalbool = false;
      this.deleteSubserviceForm = { subservice_name: "" };
    },
    closeDeleteServiceModal() {
      this.showDeleteServiceModal = false;
      this.selectedService = null;
    },
    async submitCreateServiceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/manageService",
          {
            action: "createService",
            service_name: this.createServiceForm.service_name,
            service_description: this.createServiceForm.service_description,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeCreateServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitAddSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post( "http://127.0.0.1:5000/services/manageSubService",
          {
            action: "createSubService",
            sub_name: this.addSubserviceForm.subservice_name,
            service_actual_id: this.selectedService.service_id,
            base_rate: this.addSubserviceForm.base_rate,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeAddSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitDeleteSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/manageSubService",
          {
            action: "deleteSubService",
            sub_name: this.deleteSubserviceForm.subservice_name,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeDeleteSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async deleteService() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/manageService",
          {
            action: "deleteService",
            service_name: this.selectedService.service_info.service_name
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeDeleteServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },

    showEditServiceModal(service) {
      this.editServiceForm.service_actual_id = service.service_id;
      this.editServiceForm.service_name = service.service_info.service_name;
      this.editServiceForm.service_description = service.service_info.service_desc;
      this.showEditServiceModalbool = true;
    },
    closeEditServiceModal() {
      this.showEditServiceModalbool = false;
      this.editServiceForm = { service_actual_id: null, service_name: "", service_description: "" };
    },
    showEditSubserviceModal(subservice) {
      this.editSubserviceForm.subservice_id = subservice.subservice_id;
      this.editSubserviceForm.subservice_name = subservice.subservice_name;
      this.editSubserviceForm.subservice_previous_name = subservice.subservice_name;
      this.editSubserviceForm.base_rate = subservice.base_rate;
      this.showEditSubserviceModalbool = true;
    },
    closeEditSubserviceModal() {
      this.showEditSubserviceModalbool = false;
      this.editSubserviceForm = { subservice_id: null, subservice_name: "", subservice_previous_name: "", base_rate: null };
    },
    async submitEditServiceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.put("http://127.0.0.1:5000/services/updateService",
          {
            action: "updateService",
            service_actual_id: this.editServiceForm.service_actual_id,
            service_name: this.editServiceForm.service_name,
            service_description: this.editServiceForm.service_description,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeEditServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitEditSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.put("http://127.0.0.1:5000/services/updateService",
          {
            action: "updateSubService",
            subservice_id: this.editSubserviceForm.subservice_id,
            subservice_name: this.editSubserviceForm.subservice_name,
            subservice_previous_name: this.editSubserviceForm.subservice_previous_name,
            base_rate: this.editSubserviceForm.base_rate,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeEditSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
  

  },
  created() {
    this.fetchServices();
  }
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
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.header-icon {
  font-size: 2.5rem;
}

.title-group h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.title-group p {
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
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
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  transition: box-shadow 0.3s;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: white;
  color: #4CAF50;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

.services-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.subservices-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-icon {
  font-size: 1.5rem;
  color: #4CAF50;
}

.section-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
  }

  .header-actions {
    flex-direction: column;
    width: 100%;
  }

  .search-box {
    width: 100%;
    max-width: none;
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }
}

/* Add these styles for the service cards */
.services-grid {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 0.5rem;
  scroll-padding: 1rem;
}

.service-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
  min-width: 300px;
  flex-shrink: 0;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.service-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.25rem;
}

.service-date {
  color: #666;
  font-size: 0.875rem;
}

.service-description {
  color: #4a5568;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.add-btn {
  background: #4CAF50;
  grid-column: span 2;
}

.add-btn:hover {
  background: #43a047;
}

.edit-btn {
  background: #2196F3;
}

.edit-btn:hover {
  background: #1e88e5;
}

.remove-btn {
  background: #FF9800;
}

.remove-btn:hover {
  background: #f57c00;
}

.view-btn {
  background: #9C27B0;
}

.view-btn:hover {
  background: #8e24aa;
}

.delete-btn {
  background: #f44336;
  grid-column: span 2;
}

.delete-btn:hover {
  background: #e53935;
}

/* Custom scrollbar for services grid */
.services-grid::-webkit-scrollbar {
  height: 8px;
}

.services-grid::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.services-grid::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

.services-grid::-webkit-scrollbar-thumb:hover {
  background: #43a047;
}

@media (max-width: 768px) {
  .service-card {
    min-width: 100%;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .add-btn, .delete-btn {
    grid-column: auto;
  }
}

/* Modal styles */
.modal-content {
  color: #2c3e50;
}

.modal-header {
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.modal-title {
  color: #2c3e50;
  font-weight: 600;
}

.modal-body {
  color: #4a5568;
}

.form-group label {
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  color: #2c3e50;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.8rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  outline: none;
}

.modal-footer {
  border-top: 1px solid #eee;
  padding: 1rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.close {
  color: #666;
  opacity: 1;
  transition: color 0.3s;
}

.close:hover {
  color: #2c3e50;
}

/* Modal backdrop */
.modal.fade.show {
  background: rgba(0, 0, 0, 0.5);
}
</style>
















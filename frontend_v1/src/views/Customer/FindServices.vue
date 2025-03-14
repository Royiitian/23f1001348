<!-- CHANGED -->
<template>
  <div class="modern-services-wrapper">
    <header class="modern-header">
      <div class="header-content">
        <div class="title-wrapper">
          <h1 class="main-title">Explore Services</h1>
          <p class="subtitle">Find the perfect service for your needs</p>
        </div>
        <div class="search-wrapper">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input
              id="search-input"
              type="text"
              class="modern-search"
              placeholder="Search services..."
              v-model="searchQuery"
              aria-label="Search services or subservices"
            />
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <section class="services-showcase" v-if="processedServices.length">
        <div class="service-cards-container">
          <article
            v-for="service in processedServices"
            :key="service.service_id"
            class="modern-service-card"
            @click="toggleSubservices(service.service_id)"
            tabindex="0"
            role="button"
            :aria-expanded="selectedService && selectedService.service_id === service.service_id"
            :aria-controls="`subservices-${service.service_id}`"
          >
            <div class="card-inner">
              <i class="fas fa-tools service-icon"></i>
              <h2 class="service-title">{{ service.service_info.service_name }}</h2>
              <p class="service-description">{{ service.service_info.service_desc }}</p>
              <span class="service-date">Added {{ service.service_info.date_created }}</span>
            </div>
          </article>
        </div>
      </section>
      <div v-else-if="loading" class="loading-state">
        <div class="loader"></div>
        <p>Loading available services...</p>
      </div>
      <div v-else class="empty-state">
        <i class="fas fa-box-open empty-icon"></i>
        <p>No services available at the moment.</p>
      </div>

      <section v-if="selectedService" class="subservices-section" :id="`subservices-${selectedService.service_id}`">
        <h3 class="section-title">
          <i class="fas fa-list-ul"></i>
          {{ selectedService.service_info.service_name }} Subservices
        </h3>
        <div class="modern-table-wrapper">
          <table class="modern-table">
            <thead>
              <tr>
                <th>Service Type</th>
                <th>Starting Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="subservice in filteredSubservices" :key="subservice.subservice_id">
                <td>{{ subservice.subservice_name }}</td>
                <td class="price-cell">${{ subservice.base_rate }}</td>
                <td>
                  <button @click="viewServicemen(subservice)" class="action-button">
                    <i class="fas fa-users"></i> View Providers
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="selectedSubservice" class="providers-section">
        <h3 class="section-title">
          <i class="fas fa-user-tie"></i>
          Available Providers for {{ selectedSubservice.subservice_name }}
        </h3>
        <div class="modern-table-wrapper" v-if="approvedServicemen.length">
          <table class="modern-table providers-table">
            <thead>
              <tr>
                <th @click="sortTable('full_name')">
                  Provider Name 
                  <i :class="getSortIconClass('full_name')"></i>
                </th>
                <th @click="sortTable('average_rating')">
                  Rating
                  <i :class="getSortIconClass('average_rating')"></i>
                </th>
                <th @click="sortTable('experience')">
                  Experience
                  <i :class="getSortIconClass('experience')"></i>
                </th>
                <th @click="sortTable('pin_code')">
                  Location
                  <i :class="getSortIconClass('pin_code')"></i>
                </th>
                <th>Request</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="person in approvedServicemen" :key="person.user_id">
                <td>{{ person.full_name }}</td>
                <td class="rating-cell">
                  <span class="rating">
                    {{ person.average_rating !== null ? person.average_rating + '★' : 'New' }}
                  </span>
                </td>
                <td>{{ person.experience }} years</td>
                <td>{{ person.pin_code }}</td>
                <td>
                  <button @click="requestServiceman(person.user_id, person.full_name)" 
                          class="request-button">
                    <i class="fas fa-paper-plane"></i> Request
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">
          <i class="fas fa-user-slash empty-icon"></i>
          <p>No providers available for this service yet.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rawServices: [],
      allServicemen: [],
      selectedService: null,
      selectedSubservice: null,
      loading: true,
      searchQuery: '',
      sortKey: '',
      sortAsc: true,
      customerApproved: false,
    };
  },
  computed: {
    processedServices() {
      const searchLower = this.searchQuery.toLowerCase();
      return this.rawServices.filter((service) => {
        const serviceMatch = 
          service.service_info.service_name.toLowerCase().includes(searchLower) ||
          service.service_info.service_desc.toLowerCase().includes(searchLower);
        
        const subserviceMatch = service.subservices.some(subservice => 
          subservice.subservice_name.toLowerCase().includes(searchLower)
        );

        return serviceMatch || subserviceMatch;
      });
    },
    filteredSubservices() {
      if (!this.selectedService) return [];
      
      const searchLower = this.searchQuery.toLowerCase();
      return this.selectedService.subservices.filter(subservice => 
        subservice.subservice_name.toLowerCase().includes(searchLower)
      );
    },
    approvedServicemen() {
      return this.allServicemen
        .filter(serviceman => 
          serviceman.service === this.selectedSubservice.subservice_name && serviceman.approval == "1"
        )
        .sort((a, b) => {
          const modifier = this.sortAsc ? 1 : -1;
          if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
          if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
          return 0;
        });
    },
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      try {
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          "http://127.0.0.1:5000/services/fetchAllServices",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        if (Array.isArray(response.data)) {
          this.rawServices = response.data;
        } else {
          console.error("Unexpected data format:", response.data);
          this.rawServices = [];
        }
      } catch (error) {
        console.error("Error fetching services:", error);
        this.rawServices = [];
      } finally {
        this.loading = false;
      }
    },
    async fetchServicemen() {
      try {
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          "http://127.0.0.1:5000/users/fetch-servicemen",
          {
            headers: {
              "Content-Type": "application/json",
              'Authorization': `${token}`,
            },
          }
        );
        if (Array.isArray(response.data)) {
          this.allServicemen = response.data;
          await this.fetchAverageRatings();
        } else {
          console.error("Unexpected data format:", response.data);
          this.allServicemen = [];
        }
      } catch (error) {
        console.error("Error fetching servicemen:", error);
        this.allServicemen = [];
      }
    },
    async fetchAverageRatings() {
      try {
        const token = localStorage.getItem("cust_Token");
        const ratingPromises = this.allServicemen.map(async (serviceman) => {
          try {
            const response = await axios.get(
              `http://127.0.0.1:5000/requests/calculateAverageRating/${serviceman.user_id}`,
              {
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `${token}`
                },
              }
            );
            if (response.data && response.data.average_rating !== undefined) {
              serviceman.average_rating = response.data.average_rating;
            } else {
              serviceman.average_rating = "No ratings available";
            }
          } catch (error) {
            console.error(`Error fetching rating for serviceman ${serviceman.user_id}:`, error);
            serviceman.average_rating = "Error";
          }
        });

        await Promise.all(ratingPromises);
      } catch (error) {
        console.error("Error fetching average ratings:", error);
      }
    },
    toggleSubservices(serviceId) {
      if (this.selectedService && this.selectedService.service_id === serviceId) {
        this.selectedService = null;
      } else {
        this.selectedService = this.rawServices.find(service => service.service_id === serviceId);
        this.searchQuery = '';
      }
      this.selectedSubservice = null;
    },
    viewServicemen(subservice) {
      this.selectedSubservice = subservice;
    },
    async requestServiceman(userId, serviceman_name) {
      if (!this.customerApproved) {
        alert("You are not approved to make service requests. Please contact support for assistance.");
        return;
      }

      try {
        const token = localStorage.getItem("cust_Token");
        const customerId = localStorage.getItem("cust_id");
        const customerName = localStorage.getItem("cust_Fullname");
        const customerAddress = localStorage.getItem("cust_pin");
        const requestData = {
          customer_id: customerId,
          serviceman_id: userId,
          status: "requested",
          service: this.selectedSubservice.subservice_name,
          serviceman_Fullname: serviceman_name,
          customer_name: customerName,
          customer_address: customerAddress,
          subservice_id: this.selectedSubservice.subservice_id
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/requests/createServiceRequest",
          requestData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );

        if (response.status === 201) {
          alert("Service request submitted successfully!");
        } else {
          alert("Failed to submit service request. Please try again.");
        }
      } catch (error) {
        console.error("Error submitting service request:", error);
        alert("An Error occurred while submitting the request!");
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
    getSortIconClass(key) {
      if (this.sortKey === key) {
        return this.sortAsc ? 'fas fa-sort-up' : 'fas fa-sort-down';
      }
      return '';
    },
  },
  created() {
    this.fetchServices();
    this.fetchServicemen();
    this.customerApproved = localStorage.getItem("cust_approval") == 1;
  },
};
</script>

<style scoped>
.modern-services-wrapper {
  background-color: #f8faf8;
  min-height: 100vh;
  color: #2c3e50;
}

.modern-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 2rem;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-top: 0.5rem;
}

.search-wrapper {
  margin-top: 1.5rem;
}

.search-box {
  position: relative;
  max-width: 500px;
}

.modern-search {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: none;
  border-radius: 50px;
  background: white;
  color: #2c3e50;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #4CAF50;
}

.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.service-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.modern-service-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  overflow: hidden;
}

.modern-service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.card-inner {
  padding: 1.5rem;
}

.service-icon {
  font-size: 2rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.service-title {
  font-size: 1.25rem;
  margin: 0.5rem 0;
  color: #2c3e50;
}

.service-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.modern-table-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-top: 1.5rem;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  background: #f5f5f5;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
}

.modern-table td {
  padding: 1rem;
  border-top: 1px solid #eee;
}

.action-button, .request-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover, .request-button:hover {
  background: #45a049;
}

.section-title {
  color: #2c3e50;
  font-size: 1.5rem;
  margin: 2rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rating-cell {
  color: #f39c12;
  font-weight: 600;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4CAF50;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  color: #ddd;
  margin-bottom: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .service-cards-container {
    grid-template-columns: 1fr;
  }
  
  .modern-table-wrapper {
    overflow-x: auto;
  }
  
  .modern-header {
    padding: 1rem;
  }
  
  .main-title {
    font-size: 2rem;
  }
}
</style>
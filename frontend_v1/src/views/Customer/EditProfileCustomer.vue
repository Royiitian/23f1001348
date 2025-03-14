<!-- CHANGED -->
<template>
  <div class="profile-edit-container">
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Loading your profile...</p>
    </div>

    <div v-else class="content-wrapper">
      <div class="profile-header">
        <i class="fas fa-user-edit header-icon"></i>
        <h1 class="profile-title">Edit Your Profile</h1>
        <p class="profile-subtitle">Update your personal information</p>
      </div>

      <div class="form-section">
        <form @submit.prevent="updateProfile" class="modern-form">
          <div class="form-grid">
            <div class="form-column">
              <div class="input-group">
                <label for="password">
                  <i class="fas fa-lock"></i>
                  New Password
                </label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  placeholder="Leave blank to keep current"
                  class="modern-input"
                >
              </div>

              <div class="input-group">
                <label for="email">
                  <i class="fas fa-envelope"></i>
                  Email Address
                </label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="mail" 
                  class="modern-input"
                  required
                >
              </div>

              <div class="input-group">
                <label for="mobile">
                  <i class="fas fa-mobile-alt"></i>
                  Mobile Number
                </label>
                <input 
                  type="tel" 
                  id="mobile" 
                  v-model="mobile" 
                  class="modern-input"
                  required
                >
              </div>
            </div>

            <div class="form-column">
              <div class="input-group">
                <label for="fullName">
                  <i class="fas fa-user"></i>
                  Full Name
                </label>
                <input 
                  type="text" 
                  id="fullName" 
                  v-model="fullName" 
                  class="modern-input"
                  required
                >
              </div>

              <div class="input-group">
                <label for="address">
                  <i class="fas fa-home"></i>
                  Address
                </label>
                <input 
                  type="text" 
                  id="address" 
                  v-model="address" 
                  class="modern-input"
                  required
                >
              </div>

              <div class="input-group">
                <label for="pinCode">
                  <i class="fas fa-map-marker-alt"></i>
                  Pin Code
                </label>
                <input 
                  type="text" 
                  id="pinCode" 
                  v-model="pinCode" 
                  class="modern-input"
                  required
                >
              </div>
            </div>
          </div>

          <div class="button-group">
            <button type="submit" class="action-button update-btn">
              <i class="fas fa-save"></i> Save Changes
            </button>
            <button type="button" class="action-button cancel-btn" @click="cancel">
              <i class="fas fa-times"></i> Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="alertMessage" class="modern-alert" :class="alertClass">
      <div class="alert-content">
        <i class="fas" :class="alertIcon"></i>
        <span>{{ alertMessage }}</span>
        <button class="close-alert" @click="alertMessage = ''">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      password: '',
      mail: '',
      mobile: '',
      fullName: '',
      address: '',
      pinCode: '',
      alertMessage: '',
      alertClass: '',
      isLoading: true,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async fetchUserData() {
      try {
        const customerId = localStorage.getItem('cust_id');
        const response = await axios.get(`http://127.0.0.1:5000/users/fetch-customer/${customerId}`, {
          headers: {
            'Authorization': `${localStorage.getItem('cust_Token')}`,
          },
        });
        const customerData = response.data;
        
        // Update to handle the JSON response directly
        this.mail = customerData.mail;
        this.mobile = customerData.mobile;
        this.fullName = customerData.full_name;
        this.address = customerData.address;
        this.pinCode = customerData.pin_code;

        console.log('Fetched customer data:', customerData);
      } catch (error) {
        console.error("Error fetching customer data:", error);
        this.showAlert("Unable to fetch customer data", "alert-danger");
      } finally {
        this.isLoading = false;
      }
    },

    async updateProfile() {
      const formData = new FormData();
      if (this.password) formData.append('password', this.password);
      formData.append('mail', this.mail);
      formData.append('mobile', this.mobile);
      formData.append('full_name', this.fullName);
      formData.append('address', this.address);
      formData.append('pin_code', this.pinCode);

      try {
        const response = await axios.put('http://127.0.0.1:5000/users/modify-profile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `${localStorage.getItem('cust_Token')}`
          },
        });
        this.showAlert(response.data.message, 'alert-success');
      } catch (error) {
        console.error('Update error:', error);
        this.showAlert('An error occurred during profile update', 'alert-danger');
      }
    },
    cancel() {
      this.router.push('/Custdash/SearchServices');
    },
    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = `alert ${alertClass} alert-dismissible fade show`;
      setTimeout(() => {
        this.alertMessage = '';
      }, 5000);
    },
  },
  mounted() {
    this.fetchUserData();
  }
};
</script>

<style scoped>
.profile-edit-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-wrapper {
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.header-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.profile-title {
  font-size: 2rem;
  margin: 0;
  font-weight: 600;
}

.profile-subtitle {
  opacity: 0.9;
  margin-top: 0.5rem;
}

.form-section {
  padding: 2rem;
}

.modern-form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.input-group label i {
  margin-right: 0.5rem;
  color: #4CAF50;
}

.modern-input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.modern-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  outline: none;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.action-button {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.update-btn {
  background: #4CAF50;
  color: white;
}

.cancel-btn {
  background: #e0e0e0;
  color: #333;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #4CAF50;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.modern-alert {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 2rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.close-alert {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0.5rem;
}

.alert-success {
  background: #4CAF50;
  color: white;
}

.alert-danger {
  background: #f44336;
  color: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@media (max-width: 768px) {
  .profile-edit-container {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .button-group {
    flex-direction: column;
  }

  .modern-alert {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
  }
}
</style>
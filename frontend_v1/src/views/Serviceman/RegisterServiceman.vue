<template>
  <div class="registration-container">
    <div class="content-wrapper">
      <div class="registration-header">
        <i class="fas fa-user-plus header-icon"></i>
        <h1 class="header-title">Service Provider Registration</h1>
        <p class="header-subtitle">Join our professional service network</p>
      </div>

      <form @submit.prevent="registerUser" class="modern-form">
        <div class="form-grid">
          <div class="form-section">
            <div class="input-group">
              <label for="username">
                <i class="fas fa-user"></i>
                Username
              </label>
              <input 
                type="text" 
                id="username" 
                v-model="username" 
                class="modern-input"
                maxlength="30" 
                required
              >
            </div>

            <div class="input-group">
              <label for="password">
                <i class="fas fa-lock"></i>
                Password
              </label>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                class="modern-input"
                minlength="8"
                required
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

            <div class="input-group">
              <label for="fullName">
                <i class="fas fa-id-card"></i>
                Full Name
              </label>
              <input 
                type="text" 
                id="fullName" 
                v-model="fullName" 
                class="modern-input"
                maxlength="60"
                required
              >
            </div>

            <div class="input-group">
              <label for="address">
                <i class="fas fa-home"></i>
                Address
              </label>
              <textarea 
                id="address" 
                v-model="address" 
                class="modern-textarea"
                maxlength="500"
                required
              ></textarea>
            </div>
          </div>

          <div class="form-section">
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
                maxlength="6"
                pattern="[0-9]*"
                required
              >
            </div>

            <div class="input-group">
              <label for="service">
                <i class="fas fa-tools"></i>
                Service Category
              </label>
              <select 
                id="service" 
                v-model="selectedService" 
                @change="updateSubservices" 
                class="modern-select"
                required
              >
                <option value="">Select a service</option>
                <option 
                  v-for="service in availableServices" 
                  :key="service.service_id" 
                  :value="service"
                >
                  {{ service.service_info.service_name }}
                </option>
              </select>
            </div>

            <div class="input-group" v-if="subservices.length > 0">
              <label for="subservice">
                <i class="fas fa-list"></i>
                Specialization
              </label>
              <select 
                id="subservice" 
                v-model="selectedSubservice" 
                class="modern-select"
                required
              >
                <option value="">Select a subservice</option>
                <option 
                  v-for="subservice in subservices" 
                  :key="subservice.subservice_id" 
                  :value="subservice"
                >
                  {{ subservice.subservice_name }}
                </option>
              </select>
            </div>

            <div class="input-group">
              <label for="experience">
                <i class="fas fa-briefcase"></i>
                Years of Experience
              </label>
              <input 
                type="number" 
                id="experience" 
                v-model="experience" 
                class="modern-input"
                min="0"
                required
              >
            </div>

            <div class="input-group">
              <label for="portfolio">
                <i class="fas fa-file-upload"></i>
                Portfolio Document
              </label>
              <div class="file-input-wrapper">
                <input 
                  type="file" 
                  id="portfolio" 
                  @change="handleFileUpload" 
                  class="modern-file-input"
                  required
                >
                <label for="portfolio" class="file-label">
                  <i class="fas fa-upload"></i>
                  {{ portfolioFileName || 'Choose File' }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="button-group">
          <button type="submit" class="action-button register-btn" :disabled="!isFormValid">
            <i class="fas fa-user-plus"></i>
            Create Account
          </button>
          <button type="button" class="action-button cancel-btn" @click="cancel">
            <i class="fas fa-times"></i>
            Cancel
          </button>
        </div>
      </form>
    </div>

    <div v-if="alertMessage" class="modern-alert" :class="alertClass">
      <div class="alert-content">
        <i class="fas" :class="alertClass.includes('success') ? 'fa-check-circle' : 'fa-exclamation-circle'"></i>
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
      username: '',
      password: '',
      mail: '',
      mobile: '',
      fullName: '',
      address: '',
      pinCode: '',
      selectedService: null,
      selectedSubservice: null,
      experience: '',
      portfolioFile: null,
      alertMessage: '',
      alertClass: '',
      availableServices: [],
      subservices: [],
      portfolioFileName: '',
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  computed: {
    isFormValid() {
      return this.username && this.password && this.mail && this.mobile && this.fullName && 
             this.address && this.pinCode && this.selectedService && this.selectedSubservice && 
             this.experience && this.portfolioFile;
    }
  },
  methods: {
    handleFileUpload(event) {
      this.portfolioFile = event.target.files[0];
      this.portfolioFileName = this.portfolioFile ? this.portfolioFile.name : '';
    },
    async registerUser() {
      if (!this.isFormValid) {
        this.showAlert('Please fill in all required fields', 'alert-danger');
        return;
      }

      const formData = new FormData();
      formData.append('action', 'service_reg');
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('mail', this.mail);
      formData.append('mobile', this.mobile);
      formData.append('full_name', this.fullName);
      formData.append('address', this.address);
      formData.append('pin_code', this.pinCode);
      formData.append('service', this.selectedService.service_info.service_name);
      formData.append('subservice', this.selectedSubservice.subservice_name);
      formData.append('experience', this.experience);
      formData.append('portfolio', this.portfolioFile);
      
      try {
        const response = await axios.post('http://127.0.0.1:5000/users/create-user', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.showAlert(response.data, 'alert-success');
        
        setTimeout(() => {
          this.$router.push('/');
        }, 2000);  // 2000 milliseconds = 2 seconds

      } catch (error) {
        console.error('Registration error:', error);
        this.showAlert('An error occurred during registration', 'alert-danger');
      }
    },
    cancel() {
      this.$router.push('/');
    },
    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = `alert ${alertClass} alert-dismissible fade show`;
      setTimeout(() => {
        this.alertMessage = '';
      }, 5000);
    },
    async fetchAvailableServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/services/fetchAllServices');
        this.availableServices = response.data;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    updateSubservices() {
      if (this.selectedService) {
        this.subservices = this.selectedService.subservices;
      } else {
        this.subservices = [];
      }
      this.selectedSubservice = null;
    },
  },
  mounted() {
    this.fetchAvailableServices();
  }
};
</script>
  
<style scoped>
.registration-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.registration-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.header-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.header-title {
  font-size: 2rem;
  margin: 0;
  font-weight: 600;
}

.header-subtitle {
  opacity: 0.9;
  margin-top: 0.5rem;
}

.modern-form {
  padding: 2rem;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.input-group label i {
  color: #4CAF50;
}

.modern-input, .modern-select, .modern-textarea {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  background: white;
}

.modern-textarea {
  min-height: 100px;
  resize: vertical;
}

.modern-input:focus, .modern-select:focus, .modern-textarea:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  outline: none;
}

.file-input-wrapper {
  position: relative;
}

.modern-file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem;
  background: #f5f5f5;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-label:hover {
  border-color: #4CAF50;
  background: #e8f5e9;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
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

.register-btn {
  background: #4CAF50;
  color: white;
}

.cancel-btn {
  background: #e0e0e0;
  color: #333;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@media (max-width: 768px) {
  .registration-container {
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
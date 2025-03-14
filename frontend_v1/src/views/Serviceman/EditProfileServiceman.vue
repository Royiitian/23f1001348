<template>
    <div class="profile-edit-container">
        <div class="content-wrapper">
            <div class="profile-header">
                <i class="fas fa-user-cog header-icon"></i>
                <h1 class="header-title">Professional Profile</h1>
                <p class="header-subtitle">Update your service provider information</p>
            </div>

            <form @submit.prevent="updateProfile" class="modern-form">
                <div class="form-grid">
                    <div class="form-section">
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
                                required
                                min="0"
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
                    <button type="submit" class="action-button update-btn">
                        <i class="fas fa-save"></i>
                        Save Changes
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
            userId: null,
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
            portfolioFileName: '',
            alertMessage: '',
            alertClass: '',
            availableServices: [],
            subservices: [],
            maxPrice: 0,
        };
    },
    setup() {
        const router = useRouter();
        return { router };
    },
    methods: {
        handleFileUpload(event) {
            this.portfolioFile = event.target.files[0];
            this.portfolioFileName = this.portfolioFile ? this.portfolioFile.name : '';
        },
        updateSubservices() {
            if (this.selectedService) {
                this.subservices = this.selectedService.subservices;
                this.maxPrice = this.selectedService.service_info.max_price;
            } else {
                this.subservices = [];
                this.maxPrice = 0;
            }
            this.selectedSubservice = null;
        },
        async updateProfile() {
            // Check if a subservice is selected when a service is selected
            if (this.selectedService && !this.selectedSubservice) {
                this.showAlert('Please select a subservice', 'alert-danger');
                return;
            }

            const formData = new FormData();
            if (this.password) formData.append('password', this.password);
            formData.append('mail', this.mail);
            formData.append('mobile', this.mobile);
            formData.append('full_name', this.fullName);
            formData.append('address', this.address);
            formData.append('pin_code', this.pinCode);
            formData.append('service', this.selectedService ? this.selectedService.service_info.service_name : '');
            formData.append('subservice', this.selectedSubservice ? this.selectedSubservice.subservice_name : '');
            formData.append('experience', this.experience);
            if (this.portfolioFile) formData.append('portfolio', this.portfolioFile);

            try {
                const response = await axios.put('http://127.0.0.1:5000/users/modify-profile', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `${localStorage.getItem('service_Token')}`
                    },
                });
                this.showAlert(response.data.message, 'alert-success');
            } catch (error) {
                console.error('Update error:', error);
                this.showAlert('An error occurred during profile update', 'alert-danger');
            }
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
        async fetchUserData() {
            try {
                const userId = localStorage.getItem('service_id');
                if (!userId) {
                    throw new Error('User ID not found');
                }

                const response = await axios.get(`http://127.0.0.1:5000/users/fetch-serviceman/${userId}`, {
                    headers: {
                        'Authorization': `${localStorage.getItem('service_Token')}`
                    }
                });

                // Handle the JSON response directly
                const userData = response.data;
                this.userId = userData.user_id;
                this.fullName = userData.full_name;
                this.address = userData.address;
                this.pinCode = userData.pin_code;
                this.experience = userData.experience;
                this.mail = userData.mail;
                this.mobile = userData.mobile;
                
                // Find the matching service and subservice
                if (userData.service) {
                    this.selectedService = this.availableServices.find(service => 
                        service.service_info.service_name === userData.service
                    );
                    this.updateSubservices();
                    if (this.selectedService) {
                        this.selectedSubservice = this.subservices.find(subservice => 
                            subservice.subservice_name === userData.subservice
                        );
                    }
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                this.showAlert('Error fetching user data. Please try again.', 'alert-danger');
            }
        }
    },
    mounted() {
        this.fetchAvailableServices().then(() => {
            this.fetchUserData();
        });
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
    max-width: 1200px;
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

.modern-input, .modern-select {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
    background: white;
}

.modern-input:focus, .modern-select:focus {
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

.update-btn {
    background: #4CAF50;
    color: white;
}

.action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
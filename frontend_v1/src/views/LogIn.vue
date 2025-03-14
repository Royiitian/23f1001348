<template>
  <div class="login-container">
    <video autoplay loop muted class="background-video" playsinline>
      <source src="/background.mp4" type="video/mp4">
    </video>

    <div class="overlay"></div>

    <div class="dynamic-text">
      Welcome to our platform! Secure and reliable home services at your fingertips
    </div>

    <div class="content-wrapper">
      <div class="login-card">
        <div class="login-header">
          <i class="fas fa-user-circle header-icon"></i>
          <h1 class="header-title">Welcome Back</h1>
          <p class="header-subtitle">Sign in to your account</p>
        </div>

        <form @submit.prevent="login" class="modern-form">
          <div class="input-group">
            <label for="username">
              <i class="fas fa-user"></i>
              Username
            </label>
            <input type="text" id="username" v-model="username" class="modern-input" required>
          </div>

          <div class="input-group">
            <label for="password">
              <i class="fas fa-lock"></i>
              Password
            </label>
            <input type="password" id="password" v-model="password" class="modern-input" required>
          </div>

          <div class="button-group">
            <button type="submit" class="action-button login-btn">Sign In</button>
          </div>

          <div class="register-options">
            <button type="button" class="action-button customer-btn" @click="CustRegister">Register as Customer</button>
            <button type="button" class="action-button service-btn" @click="ServiceRegister">Register as Service Provider</button>
          </div>
        </form>
      </div>
    </div>
    <div v-if="alertMessage" class="modern-alert" :class="alertClass">
      <div class="alert-content">
        <i class="fas" :class="getAlertIcon"></i>
        {{ alertMessage }}
        <button class="close-alert" @click="alertMessage = ''">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 🌟 Full Page Container */
.login-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 🌟 Video Background */
.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}

/* 🌟 Dark Overlay */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 0;
}

/* 🌟 Moving Text Animation */
.dynamic-text {
  position: absolute;
  top: 20px;
  width: 100%;
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 3px;
  background: linear-gradient(90deg, #ff4b1f, #ff9068, #6dd5ed, #2193b0); /* Unique Neon Sunset Gradient */
  background-clip: text;
  -webkit-background-clip: text; /* Required for Safari & Chrome */
  -webkit-text-fill-color: transparent; /* Makes the text color follow the gradient */
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 255, 255, 0.5);
  animation: glowing 1s ease-in-out infinite alternate, wave 5s infinite linear, marquee 10s linear infinite;
  white-space: nowrap;
  overflow: hidden;
}

/* 🌟 Smooth Marquee Effect */
@keyframes marquee {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}

/* 🌟 Pulsating Glow Effect */
@keyframes glowing {
  0% { text-shadow: 0 0 10px #ff4b1f, 0 0 15px #ff9068, 0 0 20px #6dd5ed; }
  100% { text-shadow: 0 0 15px #6dd5ed, 0 0 20px #2193b0, 0 0 30px #ff4b1f; }
}

/* 🌟 Subtle Wave Effect */
@keyframes wave {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(8px); }
}


/* 🌟 Larger & More Transparent Login Card */
.login-card {
  background: transparent; /* More transparent */
  border-radius: 15px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  position: relative;
  z-index: 1;
  width: 500px; /* Increased width */
  text-align: center;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

/* 🌟 Login Header */
.login-header {
  margin-bottom: 25px;
}
.header-title {
  font-size: 2rem;
  color: #fff;
}
.header-subtitle {
  font-size: 1.1rem;
  color: #ccc;
}
.header-icon {
  font-size: 3.5rem;
  color: #ffcc00;
}

/* 🌟 Input Fields */
.input-group {
  margin-bottom: 20px;
  text-align: left;
}
.input-group label {
  display: flex;
  align-items: center;
  font-size: 1rem;
  color: #fff;
}
.input-group i {
  margin-right: 10px;
}
.modern-input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: 0.3s;
}
.modern-input:focus {
  border-color: #ffcc00;
  background: rgba(255, 255, 255, 0.2);
}

/* 🌟 Buttons (Neon Glow Effect) */
/* 🌟 Buttons (Neon Glow Effect) */
.action-button {
  width: 80%; /* Reduce width to 80% of login box */
  max-width: 250px; /* Prevent excessive stretching */
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
  text-transform: uppercase;
  display: block;
  margin: 10px auto; /* Centering */
}

/* 🔹 Login Button */
.login-btn {
  background: linear-gradient(90deg, #ff8c00, #ffcc00);
  color: #fff;
}
.login-btn:hover {
  background: linear-gradient(90deg, #ffcc00, #ff8c00);
  box-shadow: 0 0 8px #ffcc00, 0 0 25px #ffcc00;
}

/* 🔹 Customer Registration Button */
.customer-btn {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  color: #fff;
  margin-top: 12px;
}
.customer-btn:hover {
  background: linear-gradient(90deg, #0072ff, #00c6ff);
  box-shadow: 0 0 8px #00c6ff, 0 0 25px #00c6ff;
}

/* 🔹 Service Provider Registration Button */
.service-btn {
  background: linear-gradient(90deg, #28a745, #20c997);
  color: #fff;
  margin-top: 12px;
}

.service-btn:hover {
  background: linear-gradient(90deg, #20c997, #28a745);
  box-shadow: 0 0 8px #20c997, 0 0 25px #20c997;
}

/* alert styling */
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

.alert-warning {
  background: #FF9800;
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
  .login-container {
    padding: 1rem;
  }

  .register-options {
    grid-template-columns: 1fr;
  }

  .modern-alert {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
  }
}

</style>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/users/authenticate', {
          username: this.username,
          password: this.password,
        });
        if (response.data.success) {
          this.showAlert('Login Successful', 'alert-success');
          const token = response.data.token;
          const user_id = response.data.user_id;
          const full_name = response.data.full_name;
          const pin_code = response.data.pin_code;
          const approval = response.data.approval;
          const username = this.username;
          const role = response.data.role;

          if (role === 'customer') {
            setTimeout(() => {
              localStorage.setItem('cust_Token', token);
              localStorage.setItem('cust_name', username);
              localStorage.setItem('cust_id', user_id);
              localStorage.setItem('cust_Fullname', full_name);
              localStorage.setItem('cust_pin', pin_code);
              localStorage.setItem('cust_approval', approval);

              this.$router.push('/Custdash');
            }, 1000);
          } else if (role === 'serviceman') {
            setTimeout(() => {
              localStorage.setItem('service_Token', token);
              localStorage.setItem('service_name', username);
              localStorage.setItem('service_id', user_id);
              localStorage.setItem('service_Fullname', full_name);
              this.$router.push('/Servicedash');
            }, 1000);
          } else if (role === 'admin') {
            setTimeout(() => {
              localStorage.setItem('admin_Token', token);
              localStorage.setItem('admin_name', username);
              localStorage.setItem('admin_id', user_id);
              localStorage.setItem('admin_Fullname', full_name);
              this.$router.push('/adminDash');
            }, 1000);
          }
        } else {
          this.showAlert('The username entered does not exist or the password is incorrect!', 'alert-warning');
        }
      } catch (error) {
        console.error('Login error:', error);
        this.showAlert('An error occurred during login', 'alert-danger');
      }
    },
    CustRegister() {
      this.$router.push('/CustomerRegistration');
    },
    ServiceRegister() {
      this.$router.push('/ServiceRegistration');
    },
    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = `alert ${alertClass} alert-dismissible fade show`;
    }
  },
  computed: {
    getAlertIcon() {
      if (this.alertClass.includes('alert-success')) return 'fa-check-circle';
      if (this.alertClass.includes('alert-warning')) return 'fa-exclamation-triangle';
      if (this.alertClass.includes('alert-danger')) return 'fa-times-circle';
      return 'fa-info-circle';
    }
  }
};
</script>

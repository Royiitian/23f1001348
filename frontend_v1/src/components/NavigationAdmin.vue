<!-- src/components/Navbar.vue -->
<template>
  <nav class="modern-navbar">
    <div class="nav-container">
      <div class="user-info">
        <i class="fas fa-user-shield user-icon"></i>
        <span class="welcome-text">{{ welcomeMessage }}</span>
      </div>

      <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen">
        <i class="fas fa-bars"></i>
      </button>

      <div class="nav-links" :class="{ 'active': isMenuOpen }">
        <router-link to="/adminDash/Services" class="nav-item">
          <i class="fas fa-cogs"></i>
          <span>Services</span>
        </router-link>
        <router-link to="/adminDash/allRequests" class="nav-item">
          <i class="fas fa-chart-line"></i>
          <span>Statistics</span>
        </router-link>
        <router-link to="/adminDash/ApprovalCentre" class="nav-item">
          <i class="fas fa-user-check"></i>
          <span>Approvals</span>
        </router-link>
        <router-link to="/" class="nav-item" @click="deletelocal">
          <i class="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNav',
  data() {
    return {
      welcomeMessage: 'Welcome user!',
      isMenuOpen: false
    };
  },
  methods: {
    deletelocal() {
      localStorage.removeItem('admin_Token');
      localStorage.removeItem('admin_name');
      localStorage.removeItem('admin_id');
      localStorage.removeItem('admin_Fullname');
    }
  },
  mounted() {
    const uname = localStorage.getItem('admin_Fullname');
    const uid = localStorage.getItem('admin_id');
    if (uname) {
      this.welcomeMessage = `Welcome ${uname}! (ID: ${uid})`;
    }
  }
};
</script>

<style scoped>
.modern-navbar {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
}

.user-icon {
  font-size: 1.5rem;
}

.welcome-text {
  font-weight: 500;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-item i {
  font-size: 1.2rem;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #4CAF50;
    flex-direction: column;
    padding: 1rem;
    gap: 0.5rem;
  }

  .nav-links.active {
    display: flex;
  }

  .nav-item {
    width: 100%;
  }
}
</style>
<!-- 
if (response.data.role === 'admin') {
  setTimeout(() => {
    localStorage.setItem('admin_Token', token);
    localStorage.setItem('admin_name', username);
    localStorage.setItem('admin_id', user_id);
    localStorage.setItem('admin_Fullname', full_name);
    this.$router.push('/Admindash');
  }, 1000);
} -->
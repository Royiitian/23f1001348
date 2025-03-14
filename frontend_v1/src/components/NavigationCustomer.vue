<!-- src/components/Navbar.vue -->
<template>
  <nav class="modern-navbar">
    <div class="nav-container">
      <div class="user-info">
        <i class="fas fa-user user-icon"></i>
        <span class="welcome-text">{{ welcomeMessage }}</span>
      </div>

      <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen">
        <i class="fas fa-bars"></i>
      </button>

      <div class="nav-links" :class="{ 'active': isMenuOpen }">
        <router-link to="/Custdash/SearchServices" class="nav-item">
          <i class="fas fa-search"></i>
          <span>Search</span>
        </router-link>
        <router-link to="/Custdash/MyServices" class="nav-item">
          <i class="fas fa-clipboard-list"></i>
          <span>My Services</span>
        </router-link>
        <router-link to="/Custdash/Summary" class="nav-item">
          <i class="fas fa-chart-bar"></i>
          <span>Summary</span>
        </router-link>
        <router-link to="/Custdash/editProf" class="nav-item">
          <i class="fas fa-user-edit"></i>
          <span>Edit Profile</span>
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
  name: 'CustNav',
  data() {
    return {
      welcomeMessage: 'Welcome user!',
      isMenuOpen: false
    };
  },
  methods: {
    deletelocal() {
      localStorage.removeItem('cust_Token');
      localStorage.removeItem('cust_name');
      localStorage.removeItem('cust_id');
      localStorage.removeItem('cust_Fullname');
      localStorage.removeItem('cust_approval');
    }
  },
  mounted() {
    const uname = localStorage.getItem('cust_Fullname');
    const uid = localStorage.getItem('cust_id');
    const approval = localStorage.getItem('cust_approval');
    if (uname) {
      this.welcomeMessage = `Welcome ${uname}! (ID: ${uid})`;
      if (approval != 1) {
        this.welcomeMessage += " - Pending Approval";
      }
    }
  }
};
</script>

<style scoped>
/* 🌟 Futuristic Navbar with Neon Navy Blue Gradient Animation */
@keyframes gradientShift {
  0% { background: linear-gradient(135deg, #0a0f2c, #0059ff); }
  50% { background: linear-gradient(135deg, #0059ff, #0a0f2c); }
  100% { background: linear-gradient(135deg, #0a0f2c, #0059ff); }
}

.modern-navbar {
  animation: gradientShift 5s infinite alternate;
  padding: 1rem 2rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

/* 🌟 Navbar Layout */
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 🌟 User Information Styling */
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
  font-weight: 600;
  text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-right: 2.5rem;
}

/* 🌟 Animated Icon */
.user-icon {
  font-size: 1rem;
  color: #fff;
  transition: transform 0.3s ease-in-out;
}
.user-icon:hover {
  transform: scale(1.2);
}

/* 🌟 Welcome Text */
.welcome-text {
  font-weight: 500;
  white-space: nowrap;
}

/* 🌟 Navigation Links */
.nav-links {
  display: flex;
  gap: 2rem;
  margin-left: auto;
}

/* 🌟 Neon Glow Effect on Nav Items */
.nav-item {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0px 2px 5px rgba(255, 255, 255, 0.2);
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0px 0px 12px rgba(0, 89, 255, 0.7);
}

/* 🌟 Adjust Nav Icon Size */
.nav-item i {
  font-size: 1rem;
}

/* 🌟 Animated Menu Toggle for Mobile */
.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
}

.menu-toggle:hover {
  transform: rotate(90deg);
}

/* 🌟 Responsive Navbar */
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
    background: rgba(10, 15, 44, 0.95);
    flex-direction: column;
    padding: 1rem;
    gap: 0.8rem;
    border-radius: 10px;
    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  }

  .nav-links.active {
    display: flex;
  }

  .nav-item {
    width: 100%;
    text-align: center;
    padding: 1rem;
  }
}
</style>
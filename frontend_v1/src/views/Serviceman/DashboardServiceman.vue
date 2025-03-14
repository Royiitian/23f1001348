<!-- src/views/DashboardLayout.vue -->
<template>
  <div class="dashboard-layout">
    <ServicemanNav />
    <div class="container mt-4">
      <router-view></router-view> <!-- Dynamic content will be loaded here -->
    </div>
  </div>
</template>


<script>
import ServicemanNav from '@/components/NavigationServiceman.vue';


export default {
  name: 'Servicedash',
  components: {
    ServicemanNav
  },
  created() {
    this.$router.push('/Servicedash/requests');
  }
}
</script>


<style scoped>
/* 🌟 Stunning Dashboard Background */
.dashboard-layout {
  background: linear-gradient(135deg, #0a0f2c, #003366, #007FFF); /* Emerald Green Gradient */
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 10px;
}

/* 🌟 Glassmorphism Effect for Content */
.container {
  width: 85%;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.15); /* Transparent White */
  backdrop-filter: blur(15px); /* Frosted Glass Effect */
  -webkit-backdrop-filter: blur(15px);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease-in-out;
}

/* 🌟 Animated Neon Glow Header */
.container:hover {
  box-shadow: 0px 5px 25px rgba(255, 255, 255, 0.8); /* Green Neon Glow */
}

/* 🌟 Dashboard Navbar */
nav {
  background: rgba(0, 0, 0, 0.3); /* Transparent Black */
  padding: 15px;
  width: 100%;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 350;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

/* 🌟 Text Enhancements */
h1, h2, h3 {
  text-align: center;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
  font-weight: bold;
}

/* 🌟 Subtle Text Hover Effect */
h1:hover, h2:hover, h3:hover {
  text-shadow: 0 0 20px rgba(160, 160, 160, 1);
  transition: 0.3s ease-in-out;
}
</style>

<!-- src/views/DashboardLayout.vue -->
<template>
  <div class="dashboard-layout">
    <AdminNav />
    <div class="container mt-4">
      <router-view></router-view> <!-- Dynamic content will be loaded here -->
    </div>
  </div>
</template>

<script>
import AdminNav from '@/components/NavigationAdmin.vue';


export default {
  name: 'adminDash',
  components: {
    AdminNav
  },
  created() {
    this.$router.push('/adminDash/Services');
  }
}
</script>

<style scoped>
.dashboard-layout {
  background-color: #004302; /* Dark blue background */
  color: white; /* Optional: Adjust text color for better contrast */
  min-height: 100vh; /* Ensure it covers the full viewport height */
  display: flex;
  flex-direction: column;
}

.container {
  padding-top: 20px;
}
</style>

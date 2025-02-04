const routes = [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    { path: '/customer-dashboard', component: CustomerDashboard },
    { path: '/professional-dashboard', component: ProfessionalDashboard },
    { path: '/admin-dashboard', component: AdminDashboard },
    { path: '/services', component: Services },
    { path: '/bookings', component: Bookings }
  ];
  
  const router = new VueRouter({
    mode: 'history',
    routes
  });
  
  router.beforeEach((to, from, next) => {
    const publicPages = ['/', '/register'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('authToken');
    const userRole = localStorage.getItem('userRole');
  
    if (authRequired && !loggedIn) {
      return next('/');
    }
  
    if (loggedIn && publicPages.includes(to.path)) {
      return next(`/${userRole}-dashboard`);
    }
  
    next();
  });
  
  new Vue({
    router,
    el: '#app',
    data: {
      userRole: localStorage.getItem('userRole') || null
    },
    created() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.fetchUserRole(token);
      }
    },
    methods: {
      fetchUserRole(token) {
        fetch('/api/user-role', {
          headers: { 'Authentication-Token': token }
        })
          .then(response => response.json())
          .then(data => {
            this.userRole = data.role;
            localStorage.setItem('userRole', data.role);
          });
      }
    }
  });
  
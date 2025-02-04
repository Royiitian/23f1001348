const Login = {
    template: `
      <div class="row justify-content-center">
        <div class="col-md-6">
          <h2 class="text-center mb-4">Login</h2>
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="email">Email address</label>
              <input v-model="email" type="email" class="form-control" id="email" required>
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="password" type="password" class="form-control" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Login</button>
          </form>
        </div>
      </div>
    `,
    data() {
      return {
        email: '',
        password: ''
      }
    },
    methods: {
      login() {
        fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userRole', data.role);
            this.$root.userRole = data.role;
            this.redirectToDashboard(data.role);
          } else {
            alert(data.message || 'Login failed');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred during login');
        });
      },
      redirectToDashboard(role) {
        switch(role) {
          case 'customer':
            this.$router.push('/customer-dashboard');
            break;
          case 'service_professional':
            this.$router.push('/professional-dashboard');
            break;
          case 'admin':
            this.$router.push('/admin-dashboard');
            break;
          default:
            alert('Unknown user role');
        }
      }
    }
  };
  
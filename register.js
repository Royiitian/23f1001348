const Register = {
    template: `
      <div class="row justify-content-center">
        <div class="col-md-6">
          <h2 class="text-center mb-4">Register</h2>
          <form @submit.prevent="register">
            <div class="form-group">
              <label for="email">Email address</label>
              <input v-model="email" type="email" class="form-control" id="email" required>
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="password" type="password" class="form-control" id="password" required>
            </div>
            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input v-model="confirmPassword" type="password" class="form-control" id="confirmPassword" required>
            </div>
            <div class="form-group">
              <label for="role">Role</label>
              <select v-model="role" class="form-control" id="role">
                <option value="customer">Customer</option>
                <option value="service_professional">Service Professional</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Register</button>
          </form>
        </div>
      </div>
    `,
    data() {
      return {
        email: '',
        password: '',
        confirmPassword: '',
        role: 'customer'
      }
    },
    methods: {
      register() {
        if (this.password !== this.confirmPassword) {
          alert("Passwords don't match");
          return;
        }
        fetch('/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.role
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Registration successful! Please login.');
            this.$router.push('/');
          } else {
            alert(data.message || 'Registration failed');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred during registration');
        });
      }
    }
  };
  
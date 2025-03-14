import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap'
window.bootstrap = require('bootstrap/dist/js/bootstrap.bundle.js');

// import { Bar } from 'vue-chartjs';
// import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);


// Import jQuery
import $ from 'jquery';

// Optionally import Popper.js (if you need to use it directly)
import Popper from '@popperjs/core';

createApp(App).use(router).mount('#app')

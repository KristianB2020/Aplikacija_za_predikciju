import Vue from 'vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css'
import VModal from 'vue-js-modal'
import App from './App.vue'
import router from './router'
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fab, fas, far);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false
Vue.use(VModal);

new Vue({
  router,
  store,
  render: h => h(App),
  components: { App },
  template: '<App/>',
  data: {
    predikcije: [],
    idusera: '',
    imeUsera: '',
    prezimeUsera: '',
    emailUsera: '',
    mobUsera: '',
    rolaUsera: '',
    lozinkaUsera: '',
  },
}).$mount('#app')

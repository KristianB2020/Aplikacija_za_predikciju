import Vue from 'vue'
import VueRouter from 'vue-router'
/*import Home from '../views/Home.vue'*/
import Pocetni from '@/components/Pocetni';
import Drzave from '@/components/Drzave';
import Sobe from '@/components/Sobe';
import Hoteli from '@/components/Hoteli';
import Useri2 from '@/components/Useri2';
import LoginFail from '@/components/LoginFail';
import Dashboard from '@/components/Dashboard';
import MojFooter from '@/components/Footer';
import DetaljiUser from '@/components/DetaljiUser';
import Predikcije from '@/components/Predikcije';
import Jedinice from '@/components/Jedinice';
import Iznosi from '@/components/Iznosi';

Vue.use(VueRouter)

  const routes = [
    {
      path: '/',
      name: 'Pocetni',
      component: Pocetni,
    },
    {
      path: '/drzave',
      name: 'Drzave',
      component: Drzave,
    },
    {
      path: '/sobe',
      name: 'Sobe',
      component: Sobe,
    },
    {
      path: '/useri2',
      name: 'Useri2',
      component: Useri2,
    },
    {
      path: '/loginfail',
      name: 'LoginFail',
      component: LoginFail,
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path: '/footer',
      name: 'MojFooter',
      component: MojFooter,
    },
    {
      path: '/hoteli',
      name: 'Hoteli',
      component: Hoteli,
    },
    {
      path: '/detaljiuser',
      name: 'DetaljiUser',
      component: DetaljiUser,
    },
    {
      path: '/predikcije',
      name: 'Predikcije',
      component: Predikcije,
    },
    {
      path: '/jedinice',
      name: 'Jedinice',
      component: Jedinice,
    },
    {
      path: '/iznosi',
      name: 'Iznosi',
      component: Iznosi,
    },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router

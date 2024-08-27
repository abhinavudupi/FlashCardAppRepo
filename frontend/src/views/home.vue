<template>
  <div class="home-page">
    <ul class="nav nav-pills justify-content-end">
      <li class="nav-item"><button id="loginbtn" type='button' class='btn btn-primary' data-bs-toggle='modal' data-bs-target='#loginModal'>Login</button></li>
      <li class="nav-item"><button type='button' class='btn btn-secondary' data-bs-toggle='modal' data-bs-target='#signupModal'>Signup</button></li>
    </ul>
    <Signup id="signupModal"></Signup>
    <Login id="loginModal"></Login>
    <About/>
  </div>
</template>

<script>
import About from '../components/about.vue'
import Signup from '../components/signup.vue'
import Login from '../components/login.vue'
export default {
  name: 'Home',
  components:{
    Signup,
    Login,
    About
  }
}
</script>

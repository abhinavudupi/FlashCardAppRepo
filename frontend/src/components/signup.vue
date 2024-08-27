<template>
  <div>
    <div
      class="modal fade"
      :id="id"
      tabindex="-1"
      aria-labelledby="signupModal"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header mh">
            <h5 class="modal-title" id="exampleModalLabel"></h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="signup">
              <h1>Sign Up</h1>
              <form
                @submit.prevent="submitForm"
                v-bind:class="{ 'was-validated': error }"
              >
                <div class="form-floating mb-3 mt-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="username"
                    placeholder="Username"
                    name="username"
                    required
                  />
                  <label for="username">Username</label>
                  <!-- <div class="valid-feedback">Valid.</div>
                    <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                    type="email"
                    class="form-control"
                    v-model="email"
                    placeholder="Email ID"
                    name="email"
                    required
                  />
                  <label for="email">Email ID</label>
                  <!-- <div class="valid-feedback">Valid.</div>
                    <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                    id="pwd1"
                    type="password"
                    class="form-control"
                    v-model="password"
                    placeholder="Password"
                    name="password"
                    required
                  />
                  <label for="password">Password</label>
                  <!-- <div class="valid-feedback">Valid.</div>
                    <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                    id="pwd2"
                    type="password"
                    class="form-control"
                    v-model="ndpassword"
                    placeholder="Reenter Password"
                    name="password2"
                    required
                  />
                  <label for="password2">Re-enter password</label>
                  <!-- <div class="valid-feedback">Valid.</div>
                    <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <button class="btn btn-primary" type="submit">Sign Up</button>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="close-signup-modal"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Signup",
  props: ["id"],
  data() {
    return {
      username: "",
      email: "",
      password: "",
      ndpassword: "",
      error: false,
    };
  },
  methods: {
    validateForm(){
      if (this.password == this.ndpassword){
        return true}
      else{
        this.error = true
        this.password=''
        this.ndpassword=''
        alert('Passwords must match')
        return false}
    },
    async submitForm() {
      if(this.validateForm()){
      const res = fetch("http://10.1.1.43:8080/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
          email: this.email,
        }),
      });
      res
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            this.error = false;
            document.getElementById("close-signup-modal").click();
            sessionStorage.setItem("access token", data["access token"]);
            sessionStorage.setItem("uid", data["user_id"]);
            sessionStorage.setItem("un", data["username"]);
            this.$router.push({ path: "/dashboard" });
          } else if (data["status"] == "error") {
            this.username = "";
            this.password = "";
            this.ndpassword = "";
            this.email = "";
            this.error = true;
            alert("error : "+data["message"]);
          }
        });}
        else{
          console.log('error')
        }
    },
  },
};
</script>

<style scoped>
.mh {
  background-color: cadetblue;
  opacity: 80%;
}
</style>
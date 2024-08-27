<template>
  <div>
    <div
      class="modal fade"
      :id="id"
      tabindex="-1"
      aria-labelledby="loginModal"
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
            <div class="login">
              <h1>Log In</h1>
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
                  <!-- <div class="valid-feedback"></div> -->
                  <!-- <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                    id="pwd"
                    type="password"
                    class="form-control"
                    v-model="password"
                    placeholder="Password"
                    name="password"
                    required
                  />
                  <label for="password">Password</label>
                </div>
                <div v-if="error" class="alert alert-warning">
                  Incorrect Username or Password entered
                </div>
                <button class="btn btn-primary" type="submit">Submit</button>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="close-login-modal"
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
// import $ from "jquery";
export default {
  name: "Login",
  props: ["id"],
  data() {
    return {
      username: "",
      password: "",
      error: false,
    };
  },
  methods: {
    async submitForm() {
      const res = fetch("http://10.1.1.43:8080/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });
      res
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            this.error = false;
            document.getElementById("close-login-modal").click();
            sessionStorage.setItem("access token", data["access token"]);
            sessionStorage.setItem("un", data["username"]);
            sessionStorage.setItem("uid", data["user_id"]);
            this.$router.push({ path: "/dashboard" });
          } else if (data["status"] == "error") {
            this.username = "";
            this.password = "";
            this.error = true;
          }
        });
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
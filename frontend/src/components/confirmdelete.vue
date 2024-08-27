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
              <h1>Confirm Delete?</h1>
        <button type="button" class="btn btn-primary"  data-bs-dismiss="modal" @click="deleted">
          Confirm
        </button>
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
  methods:{
    deleted(){
      this.$parent.deletedeck(sessionStorage.getItem('did'))
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
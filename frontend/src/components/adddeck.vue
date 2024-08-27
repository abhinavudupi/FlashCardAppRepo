<template>
  <div>
    <div
      class="modal fade"
      :id="id"
      tabindex="-1"
      aria-labelledby="adddeckmodal"
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
              <h1>Add deck</h1>
              <form
                @submit.prevent="submitForm"
              >
                <div class="form-floating mb-3 mt-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="dn"
                    placeholder="New deck name"
                    name="deckname"
                    required
                  />
                  <label for="deckname">Deck Name</label>
                  <!-- <div class="valid-feedback"></div> -->
                  <!-- <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <button class="btn btn-primary" type="submit">Submit</button>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="close-adddeck-modal"
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
  name: "addDeck",
  props: ["id"],
  data() {
    return {
      deckname: "",
      dn:"",
    };
  },
  methods: {
    async submitForm() {
        this.deckname=this.dn
        this.dn=''
      const res = fetch("http://10.1.1.43:8080/api/decks?user_id="+sessionStorage.getItem('uid').toString(), {
        method: "POST",
      headers: { "Content-Type": "application/json",
                  "APItoken": sessionStorage.getItem("access token"),
      },
        body: JSON.stringify({
          deck_name: this.deckname,
        }),
      });
      res
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            document.getElementById("close-adddeck-modal").click();
            this.$parent.updatedeck()
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
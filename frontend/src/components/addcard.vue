<template>
  <div>
    <div
      class="modal fade"
      :id="id"
      tabindex="-1"
      aria-labelledby="addcardmodal"
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
                    v-model="fn"
                    placeholder="New card front value"
                    name="cardfront"
                    required
                  />
                  <label for="cardfront">Front</label>
                  <!-- <div class="valid-feedback"></div> -->
                  <!-- <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <div class="form-floating mb-3 mt-3">
                  <input
                    type="text"
                    class="form-control"
                    v-model="bn"
                    placeholder="New card front value"
                    name="cardback"
                    required
                  />
                  <label for="cardback">Back</label>
                  <!-- <div class="valid-feedback"></div> -->
                  <!-- <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <button class="btn btn-primary" type="submit">Submit</button>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="close-addcard-modal"
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
  name: "addCard",
  props: ["id"],
  data() {
    return {
      front:"",
      back:"",
      fn:"",
      bn:""
    };
  },
  methods: {
    async submitForm() {
        this.front=this.fn
        this.back=this.bn
        this.fn=''
        this.bn=''
        console.log('submitting card')
      const res = fetch("http://10.1.1.43:8080/api/cards?user_id="+sessionStorage.getItem('uid').toString(), {
        method: "POST",
      headers: { "Content-Type": "application/json",
                  "APItoken": sessionStorage.getItem("access token"),
      },
        body: JSON.stringify({
          front: this.front,
          back: this.back,
          deck_id:this.$parent.did,
        }),
      });
      res
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            document.getElementById("close-addcard-modal").click();
            this.$parent.updatedeck()
          } else if (data["status"] == "error") {
            this.front = "error";
            this.back = data['message'];
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
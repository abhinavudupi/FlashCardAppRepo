<template>
  <div>
    <div
      class="modal fade"
      :id="id"
      tabindex="-1"
      aria-labelledby="importdeckmodal"
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
            <div class="deckimport">
              <h1>Import deck</h1>
              <form @submit.prevent="submitForm">
                <div class="mb-3 mt-3">
                  <label for="deckcsv" class="form-label"
                    >Select CSV file in specified format</label
                  >
                  <input
                    type="file"
                    class="form-control"
                    placeholder="deck csv file"
                    name="deckcsv"
                    id="deckcsv"
                    accept=".csv"
                    required
                    multiple
                  />
                  <!-- <div class="invalid-feedback">Please fill out this field.</div> -->
                </div>
                <button class="btn btn-primary" type="submit">Submit</button>
              </form>
              <div style="margin-top: 25px">
                Click
                <span><button class="btn btn-light">HERE</button></span> for
                downloading format of CSV
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="close-importdeck-modal"
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
  name: "importDeck",
  props: ["id"],
  data() {
    return {};
  },
  methods: {
    async submitForm() {
      // document.getElementById("close-importdeck-modal").click();
      const input = document.getElementById("deckcsv");
      // console.log(input.files)
      var data = new FormData();
      for (const file of input.files) {
        data.append("files[]", file, file.name);
      }
      const res = fetch(
        "http://10.1.1.43:8080/api/decks/import?user_id=" +
          sessionStorage.getItem("uid").toString(),
        {
          method: "POST",
          headers: { APItoken: sessionStorage.getItem("access token") },
          body: data
        }
      );
        res
          .then((response) => response.json())
          .then((data) => {
            if (data["status"] == "success") {
              document.getElementById("close-importdeck-modal").click();
              this.$parent.updatedeck()
            } else if (data["status"] == "error") {
              console.log(data['message'])
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
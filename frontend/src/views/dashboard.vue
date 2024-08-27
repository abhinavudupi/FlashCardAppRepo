<template>
  <div class="dashboard">
    <ul class="nav nav-pills">
      <li class="nav-item">
        <button type="button" class="btn btn-secondary" @click="goHome">
          Home
        </button>
        <button type="button" class="btn btn-primary" @click="logout">
          Logout
        </button>
      </li>
    </ul>
    <div class="grid-container">
      <div class="grid-child zero"></div>
      <div class="grid-child one"><h1>Dashboard</h1></div>
      <div class="grid-child two">
        <h2>User : {{ username }}</h2>
      </div>
    </div>

    <table class="table table-bordered table-hover" id="dashboardtable">
      <thead>
        <tr id="headerrow">
          <th>Sno</th>
          <th>Deck name</th>
          <th>Score</th>
          <th>No. of Cards</th>
          <th>Last Reviewed</th>
          <th>Review</th>
          <th>Delete</th>
          <th>Export</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in decks" :key="item.deck_id">
          <td @click="openDeck(item['deck_id'])">{{ index + 1 }}</td>
          <td @click="openDeck(item['deck_id'])">{{ item["deck_name"] }}</td>
          <td @click="openDeck(item['deck_id'])">{{ item["total_score"] }}</td>
          <td @click="openDeck(item['deck_id'])">{{ item["cards"].length }}</td>
          <td @click="openDeck(item['deck_id'])">
            {{ item["last_reviewed"] }}
          </td>
          <td>
            <button
              type="button" id="reviewbtn"
              class="btn btn-labeled btn-default"
              @click.stop="reviewdeck(item['deck_id'])"
            >
              <span class="btn-label"><i class="bi bi-eye"></i></span>
            </button>
          </td>
          <td>
            <button
              type="button" id="deletebtn"
              class="btn btn-labeled btn-default"
              @click.stop="deletedeckadd(item['deck_id'])"
              data-bs-toggle="modal"
              data-bs-target="#confirmdelete"
            >
              <span class="btn-label"><i class="bi bi-trash"></i></span>
            </button>
          </td>
          <td>
            <button
              type="button" id="exportbtn"
              class="btn btn-labeled btn-default"
              @click.stop="exportdeck(item['deck_id'])"
            >
              <span class="btn-label"><i class="bi bi-download"></i></span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <confirm-delete id="confirmdelete"></confirm-delete>
    <div class="grid-container bottom-ctnr">
      <div class="grid-child"></div>
      <div class="grid-child">
        <div>
          <button
            type="button" id="adddeckbtn"
            class="btn btn-labeled btn-primary plusbtn"
            data-bs-toggle="modal"
            data-bs-target="#adddeckmodal"
          >
            <span class="btn-label"><i class="bi bi-plus"></i></span>
          </button>
        </div>
      </div>
      <div class="grid-child two">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-toggle="modal"
          data-bs-target="#importdeckmodal"
        >
          Import
        </button>
      </div>
    </div>

    <add-deck id="adddeckmodal"></add-deck>
    <import-deck id="importdeckmodal"></import-deck>
  </div>
</template>

<script>
import confirmDelete from "../components/confirmdelete.vue";
import addDeck from "../components/adddeck.vue";
import importDeck from "../components/importdeck.vue";
export default {
  name: "Dashboard",
  components: {
    confirmDelete,
    addDeck,
    importDeck,
  },
  data() {
    return {
      decks: [],
      uid: null,
      username: null,
      source: null,
    };
  },
  methods: {
    goHome() {
      this.$router.push({ path: "/" });
    },
    deletedeckadd(did) {
      sessionStorage.setItem("did", did);
    },
    logout() {
      sessionStorage.removeItem("access token");
      sessionStorage.removeItem("uid");
      this.$router.push({ path: "/" });
    },
    openDeck(did) {
      sessionStorage.setItem("did", did);
      this.$router.push({ path: "/deckview" });
    },
    deletedeck(did) {
      const res = fetch(
        "http://10.1.1.43:8080/api/decks/" +
          did.toString() +
          "?user_id=" +
          this.uid.toString(),
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            APItoken: sessionStorage.getItem("access token"),
          },
        }
      );
      res
        .then((response) => response.json())
        .then((data) => {
          this.updatedeck();
        });
    },
    updatedeck() {
      const res1 = fetch(
        "http://10.1.1.43:8080/api/user/decks/" + this.uid.toString(),
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            APItoken: sessionStorage.getItem("access token"),
          },
        }
      );
      this.decks = [];
      res1
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            for (const i of data["data"]) {
              this.decks.push(i);
            }
          } else if (data["status"] == "error") {
            this.$router.push({ path: "/" });
          }
        });
    },
    exportdeck(did) {
      const res = fetch(
        "http://10.1.1.43:8080/api/decks/export/" +
          did.toString() +
          "?user_id=" +
          this.uid.toString(),
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            APItoken: sessionStorage.getItem("access token"),
          },
        }
      );
      res
        .then((response) => response.json())
        .then((data) => {
          // console.log(data);
        });
    },
    reviewdeck(did) {
      sessionStorage.setItem("did", did);
      this.$router.push({ path: "/review" });
    },
  },
  mounted: function () {
    this.source = new EventSource("http://10.1.1.43:8080/stream");
    this.source.addEventListener(
      "export-tasks",
      function (event) {
        var data = JSON.parse(event.data);
        alert("Export " + data.status + "\nMessage : " + data.message);
        const res = fetch(
          "http://10.1.1.43:8080/api/exports/" +
            data.file_name +
            "?user_id=" +
            sessionStorage.getItem("uid").toString(),
          {
            method: "GET",
            headers: { APItoken: sessionStorage.getItem("access token") },
          }
        );
        res
          .then((response) => response.blob())
          .then((blob) => {
            var url = window.URL.createObjectURL(blob),
            anchor = document.createElement("a");
            anchor.href = url;
            anchor.download = data.file_name;
            anchor.click();
            window.URL.revokeObjectURL(url);
          })
          .catch((err) => {
            console.log(err);
          });
      },
      false
    );
    this.source.addEventListener(
      "import-tasks",
      function (event) {
        var data = JSON.parse(event.data);
        alert("Import  " + data.status + "\nMessage : " + data.message);
        if (data.status == 'success')
        {
          location.reload()
        }
      },
      false
    );
    this.source.addEventListener(
      "error",
      function (event) {
        alert(JSON.parse(event.data));
        // alert("Failed to connect");
      },
      false
    );
    this.uid = sessionStorage.getItem("uid");
    this.username = sessionStorage.getItem("un");
    if (this.uid) {
      const res = fetch(
        "http://10.1.1.43:8080/api/user/decks/" + this.uid.toString(),
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            APItoken: sessionStorage.getItem("access token"),
          },
        }
      );
      res
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            for (const i of data["data"]) {
              this.decks.push(i);
            }
          } else if (data["status"] == "error") {
            this.$router.push({ path: "/" });
          }
        });
    } else {
      this.$router.push({ path: "/" });
    }
  },
};
</script>

<style scoped>
.btn-labeled {
  font-size: 20px;
}
.bottom-ctnr {
  margin-top: 50px;
}
.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 20px;
}
.two {
  padding: 5px;
  text-align: right;
}
.plusbtn {
  font-size: 25px;
  font-weight: bold;
  border: 0.5px black solid;
  padding: 0px;
  padding-left: 7px;
  padding-right: 7px;
}
.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 10px;
}
</style>
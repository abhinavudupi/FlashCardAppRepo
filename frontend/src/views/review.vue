<template>
  <div class="review">
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
    <div><h1>Review</h1></div>
    <div>
      <!-- <div v-for="card in deck" :key="card['card_id']">
        {{ card["back"] }}
        {{ card["front"] }}
      </div> -->
    </div>

    <div></div>

    <card-view :card="currentCard" @answered="cardAnswer"> </card-view>
  </div>
</template>

<script>
import cardView from "../components/card.vue";
export default {
  name: "review",
  components: {
    cardView,
  },
  data() {
    return {
      deck: [{ front: "", back: "" , card_id:0}],
      did: null,
      cci: 0,
    };
  },
  methods: {
    goHome() {
      this.$router.push({ path: "/" });
    },
    logout() {
      sessionStorage.removeItem("access token");
      sessionStorage.removeItem("uid");
      this.$router.push({ path: "/" });
    },
    cardAnswer(val) {
      const anss = ["10", "5", "1"];
      const res = fetch(
        "http://10.1.1.43:8080/api/cards/" +
          this.ccid.toString() +
          "?user_id=" +
          sessionStorage.getItem("uid").toString(),
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            APItoken: sessionStorage.getItem("access token"),
          },
          body: JSON.stringify({
            card_score: anss[val],
            deck_id:this.did,
          }),
        }
      );
      res
        .then((response) => response.json())
        .then((data) => {
          if (this.cci < this.deck.length - 1) {
            this.cci += 1;
          } 
          else {
            this.$router.push({ path: "/dashboard" });
          }
        });
    },
  },
  computed: {
    currentCard: function () {
      return this.deck[this.cci];
    },
    ccid:function(){
      return this.currentCard["card_id"]
    },
  },
  mounted: function () {
    this.did = sessionStorage.getItem("did");
    // this.username=sessionStorage.getItem("un")
    if (this.did) {
      const res = fetch(
        "http://10.1.1.43:8080/api/decks/cards/" +
          this.did.toString() +
          "?user_id=" +
          sessionStorage.getItem("uid").toString(),
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
            this.deck = data["data"];
            this.deck.sort(() => Math.random() - 0.5);
            if (this.deck.length == 0) {
              alert("No Cards in deck. Add cards before review")
              this.$router.push({ path: "/dashboard" });
            }
            // this.startreview();
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

<style>
</style>
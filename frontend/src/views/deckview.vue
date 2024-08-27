<template>
  <div class="deckview">
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
    <div class="grid-container"><div class="grid-child one"><h1><button type="button" class="btn btn-labeled btn-default" @click="goDashboard">
        <span class="btn-label bln"><i class="bi bi-caret-left-square-fill"></i></span></button> </h1></div>   
    <div class="grid-child two"><h1>Deck : {{cardData['deck_name']}}</h1></div><div class="grid-child zero"></div></div>
    <table class="table table-bordered table-hover" id="deckviewtable">
      <thead><tr id="headerrow">
        <th>Sno</th>
        <th>Front</th>
        <th>Back</th>
        <th>Score</th>
        <th>Edit</th>
        <th>Delete</th>
      </tr></thead>
      <tbody><tr class="" v-for="(item,index) in cardData['cards']" :key="item.card_id">
        <td>{{index+1}}</td>
        <td>{{ item['front'] }}</td>
        <td>{{ item['back'] }}</td>
        <td>{{ item['card_score'] }}</td>
        <td><button type="button" class="btn btn-labeled btn-default" @click.stop="editcard(item['card_id'])">
        <span class="btn-label"><i class="bi bi-pencil-square"></i></span></button></td>
        <td><button type="button" class="btn btn-labeled btn-default" @click.stop="deletecard(item['card_id'])">
        <span class="btn-label"><i class="bi bi-trash"></i></span></button></td>
      </tr></tbody>
    </table>
    <div>
    <button type="button" class="btn btn-labeled btn-primary plusbtn" data-bs-toggle='modal' data-bs-target='#addcardmodal'>
        <span class="btn-label"><i class="bi bi-plus"></i></span></button></div>
    <add-card id="addcardmodal"></add-card>
  </div>
</template>

<script>
import addCard from '../components/addcard.vue'
export default {
name:'DeckView',
data(){
    return{
        did:null,
        uid:null,
        cardData:[],
    }
},
components:{
  addCard,
},
methods:{
    goHome() {
      this.$router.push({ path: "/" });
    },
    logout(){
      sessionStorage.removeItem('access token')
      sessionStorage.removeItem('uid')
      this.$router.push({path:'/'})
    },
    goDashboard(){
      this.$router.push({path:'/dashboard'})
      this.$forceUpdate();
    },
    editcard(cid){
        console.log(cid)
        console.log('editing')
        // YET TO ADD EDIT CARD MODAL AND LOGIC
    },
    deletecard(cid){
      const res = fetch("http://10.1.1.43:8080/api/cards/"+cid.toString()+"?user_id="+this.uid.toString(), {
      method: "DELETE",
      headers: { "Content-Type": "application/json",
                  "APItoken": sessionStorage.getItem("access token"),
      },
    });
    res.then((response) => response.json())
      .then((data) => {this.updatedeck();})
    },
    updatedeck(){
      const res = fetch("http://10.1.1.43:8080/api/decks/"+this.did.toString()+"?user_id="+this.uid.toString(), {
    method: "GET",
    headers: { "Content-Type": "application/json",
                  "APItoken": sessionStorage.getItem("access token"),
      },
    });
    res.then((response) => response.json())
      .then((data) => {
        if (data["status"] == "success") {
          this.cardData=data['data']
        } 
        else if (data["status"] == "error") {
          this.$router.push({path:'/'})
        }
      });
    },
    
},
mounted: function () {
    this.uid=sessionStorage.getItem("uid")
    this.did=sessionStorage.getItem("did")
    const res = fetch("http://10.1.1.43:8080/api/decks/"+this.did.toString()+"?user_id="+this.uid.toString(), {
    method: "GET",
    headers: { "Content-Type": "application/json",
                  "APItoken": sessionStorage.getItem("access token"),
      },
    });
    res.then((response) => response.json())
      .then((data) => {
        if (data["status"] == "success") {
          this.cardData=data['data']
        } 
        else if (data["status"] == "error") {
          this.$router.push({path:'/'})
        }
      });
  },
}
</script>

<style scoped>
.bln{
	position: relative;
	left: -12px;
	display: inline-block;
	padding: 6px 12px;
	background: white;;
	border-radius: 3px 0 0 3px;
    font-size: 25px;
}

.btn-labeled {
	padding-top: 0;
	padding-bottom: 0;
}

.btn {
	margin-bottom: 10px;
}
  .grid-container{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr ;
    grid-gap: 20px;
  }
  .plusbtn{
    font-size: 25px;
    font-weight: bold;
    border:0.5px black solid;
    padding: 0px;
    padding-left: 7px;
    padding-right: 7px;
  }
</style>
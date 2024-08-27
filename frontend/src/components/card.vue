<template>
  <div >
    <div class="grid-container">
    <div class="grid-child"></div>
    <div @click="flip" class="flip-card grid-child one">
      <div class="flip-card-inner" v-bind:style="{transform:ca}">
        <div class="flip-card-front">
          <div id="cardtextdiv"><p id="cardtext" >{{ card["front"] }}</p></div>
        </div>
        <div class="flip-card-back">
          <div id="cardtextdiv"><p id="cardtext">{{ card["back"] }}</p></div>
        </div>
      </div>
    </div>
    <div class="grid-child"></div>
    </div>
    <button
      type="button" class="difficulty-btn btn btn-info"
      @click="() => {this.$emit('answered', '0');}">
      Easy
    </button>
    <button
      type="button" class="difficulty-btn btn btn-warning"
      @click="() => {this.$emit('answered', '1');}">
      Medium
    </button>
    <button
      type="button" class="difficulty-btn btn btn-danger"
      @click="() => {this.$emit('answered', '2');}">
      Hard
    </button>
  </div>
</template>

<script>
export default {
  name: "cardview",
  props: ["card"],
  data() {
    return {
      showback: false,
      angle:'rotateY(0deg)'
    };
  },
  computed:{
      ca: function(){
          return this.angle;
      },
  },
  watch:{
    card:function(){
      this.showback=false,
      this.angle='rotateY(0deg)'
    }
  },
  methods: {
      flip(){
          if(this.angle=='rotateY(0deg)'){this.angle='rotateY(180deg)'}
          else{this.angle='rotateY(0deg)'}
      },
  },
};
</script>

<style scoped>
.difficulty-btn{
    margin: 10px;
}
.flip-card {
  background-color: transparent;
  width: 100%;
  height: 300px;
  margin: 25px;
  position: relative;
  perspective: 1000px;
  border-radius: 15px;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  border: 4px black solid ;
  border-radius: 10px;
  transition: transform 0.3s;
  transform-style: preserve-3d;
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden; /* Safari */
  backface-visibility: hidden;
}

.flip-card-front {
  background-color:rgba(255, 248, 182, 0.986);
  color: black;
}
.flip-card-back {
  background-color:rgba(202, 197, 145, 0.986) ;
  color: black;
  transform: rotateY(180deg);
}
  .grid-container{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr ;
    grid-gap: 10px;
  }
  #cardtext{
      font-size: 70px;
      text-align: center;
      vertical-align: middle;
  }
  #cardtextdiv{
      margin-top: 15%;
      display: inline-block;
  }
</style>
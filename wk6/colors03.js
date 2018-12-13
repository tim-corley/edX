document.addEventListener('DOMContentLoaded', () => {

  // change the color of the heading when dropdown changes
  // due to use of 'this', must not use arrow function
  // 'this' is bound to what the function it is in is being called upon (color change drop-down)
  document.querySelector('#color-change').onchange = function() {
        document.querySelector('#hello').style.color = this.value;
      };
});

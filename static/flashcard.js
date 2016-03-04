function Flashcard(){
  var self = this;
  this.$flashcard = $('#flashcard');
  this.$flashcard.click(function(){
    self.flip();
  });
}

Flashcard.prototype.flip = function(){
  this.$flashcard.find('img').toggle();
  this.$flashcard.find('p').toggle();

}

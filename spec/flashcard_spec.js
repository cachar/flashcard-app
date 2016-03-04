describe("Flashcard", function () {
    var $picture, $info, flashcard;

    beforeEach(function() {
        var fixture = setFixtures(
            '<div id="flashcard">'+
            '<img id="flashcard-picture">'+
            '<p id="flashcard-text" style="display: none"></p>'+
            '</div>'
        );
        $picture = fixture.find('img');
        $info = fixture.find('p');
        flashcard = new Flashcard();
    });

    describe('#flip', function() {
        it('hides the picture', function() {
            expect($picture).toBeVisible();
            flashcard.flip();
            expect($picture).not.toBeVisible();
        });

        it('shows the text', function() {
            expect($info).not.toBeVisible();
            flashcard.flip();
            expect($info).toBeVisible();
        })

        describe('when the card is flipped again', function() {
            beforeEach(function() {
                flashcard.flip();
                flashcard.flip();
            });
            it('hides the text', function() {
                expect($info).not.toBeVisible();
            });

            it('shows the picture', function() {
                expect($picture).toBeVisible();
            });
        });
    });

    describe('when the flashcard is clicked', function() {
        beforeEach(function() {
            $('#flashcard').trigger('click');
        });

        it('hides the picture', function() {
            expect($picture).not.toBeVisible();
        });
        it('shows the text', function() {
            expect($info).toBeVisible();
        })
    });
});

/**
 * Created by hojjat on 4/28/15 AD.
 */
$(document).ready(function() {
    $('#comment').keyup(function(e) {
        if(e.which == 13) {
            var comment = $('#comment').val();
//            console.log(s=$(comment).closest('#last-media'));
//            var last = $(comment).closest('#last-media');
            var last = $('#last-media');
            var last_comment = last.prev().prev();
            var new_comment = last_comment.clone();
            var cm = new_comment.children('.media-body');
            $(cm).text(comment);
            var hr = last.prev().clone();
            var last_hr = $(last.prev());
            $(new_comment).insertAfter($(last_hr));
            $(hr).insertAfter($(new_comment));
            $('#comment').val(null);
        }
    });
});
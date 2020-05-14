$(document).ready(function() {
	$('#inputForm').on('submit', function(event) {
	    var seer = $('#seer').val();
	    var asai = $('#asai').val();
	    var word = $('#word').val().trim();
	    var meaning = $('#meaning').val().trim();
        $.ajax({
            data : {
                seer : seer,
                asai : asai,
                word : word,
                meaning : meaning
            },
            type : 'POST',
            url : '/process'
        }).done(function(data) {
            $('#resultTable tr').not(':first').remove();
            var table = '';
            $.each(JSON.parse(data.result), function(idx, obj) {
                table += '<tr><td>' + obj.word +
                        '</td><td>' + obj.meaning +
                        '</td><td>' + obj.asai +
                        '</td><td>' + obj.seer + '</td></tr>';
            });
            $('#resultTable tr').first().after(table);
            $('#status').html(data.status);
        });
		event.preventDefault();
	});
});
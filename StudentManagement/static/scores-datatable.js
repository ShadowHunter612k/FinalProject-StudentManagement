// Call the dataTables jQuery plugin
$(document).ready(function() {

  $('#scoreboard-table').DataTable({
      "columnDefs": [
    { "width": "10%", "targets": 4 }
  ]
  });
  $(".submit").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: url,
            data: form.serialize(),
           success: function(data)
           {

           }
         });

  });
  $("button").click(function(){
    $(this).find("i").removeClass("fas fa-fw fa-edit").addClass("fas fa-fw fa-ruler");
});
});


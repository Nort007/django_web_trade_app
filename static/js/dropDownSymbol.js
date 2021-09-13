function symbolValidation() {
    $("#id_account").change(function() {
    var url = $("#exchangeForm").attr("data-ajax-url");
    var exchangeId = $(this).val();
    $.ajax({
      url: url,
      data: {
        'exchange': exchangeId
      },
      success: function(data) {
        $("#id_symbol").html(data);
      }
    });
  });

}
symbolValidation();
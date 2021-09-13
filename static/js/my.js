function symbolValidation() {
    $("#id_exchange").change(function() {
    var url = $("#id_exchange").attr("data-ajax-s-url");
    var exchangeId = $(this).val();
    $.ajax({
      url: url,
      data: {
        'symbol': exchangeId
      },
      success: function(data) {
        $("#id_symbol").html(data);
      }
    });
  });
}
 symbolValidation()
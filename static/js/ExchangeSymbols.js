function exchangeSymbolValidation() {
    $("#id_account").change(function() {
    var url = $("#id_account").attr("data-ajax-s-url");
    var symbolId = $(this).val();
    $.ajax({
      url: url,
      data: {
        'symbol': symbolId
      },
      success: function(data) {
        $("#id_symbol").html(data);
      }
    });
  });

  /*$("#id_exchange").change(function() {
    var url = $("#id_exchange").attr("data-ajax-s-url");
    var exchangeId = $("#id_exchange").val();

    $.ajax({
      url: url,
      data: {
        'symbol': exchangeId
      },
      success: function(data) {
        $("#id_symbol").html(data);
      }
    });
  });*/
}

exchangeSymbolValidation();
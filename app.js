var currencyList = [['AUD', 'au'], ['BGN', 'bg'], ['BRL', 'br'], ['CAD', 'ca'], ['CHF', 'ch'], ['CZK', 'cz'], ['DKK', 'dk'], ['EUR', ''], ['GBP', 'gb'], ['HUF', 'hu'], ['JPY', 'jp'], ['NOK', 'no'], ['NZD', 'nz'], ['PLN', 'pl'], ['RON', 'ro'], ['SEK', 'se'], ['SGD', 'sg'], ['USD', 'us']];


function openDropDown(e) {
  var dropList = $($(e.target).children()[2]);
  if (dropList.css("display") === "none") {
    dropList.css("display", "block");
    $(e.currentTarget).css("border-bottom-left-radius", "0em");
    $(e.currentTarget).css("border-bottom-right-radius", "0em");

    if (dropList.children().length === 0) {
      for (var i = 0; i < currencyList.length; i++) {
        dropList.append('<div class="currency ' + i + '"><span class="flag-icon flag-icon-' + currencyList[i][1] + '"></span> ' + currencyList[i][0] + '</div>');
      }
    }
  }
}

function changeDropDownVal(e) {
  var value = $(e.target)[0].innerText;
  value = value.substring(1, value.length);

  var parent = $($($(e.target).parent()[0]).parent()[0]).children()[0];
  parent.innerText = value;
}

function callTransfer() {
  $('html, body').animate({
    scrollTop: $('.results').offset().top
  }, 1000);

  var fromCurr = $($('.dropdown')[0]).children()[0].innerText;
  var toCurr = $($('.dropdown')[1]).children()[0].innerText;
  var amount = $('#send_amount')[0].value;

  var baseURL = "http://localhost:5000/getTransfer?";
  var fromString = "from_curr=" + fromCurr;
  var toString = "&to_curr=" + toCurr;
  var amountString = "&amount=" + amount;

  var url = baseURL + fromString + toString + amountString;

  $.get(url, function(data) {
    $('.loader').css("display", "none");
  });
}

$(document).ready(function() {

  $(window).on('click', function(e) {
    if (e.target.matches('.dropdown') || e.target.matches('.fa-chevron-down')) {
      openDropDown(e);
    } else {
      $('.currency_list').css("display", "none");
    }

    if (e.target.matches('.currency')) {
      changeDropDownVal(e);
    }

    if (e.target.matches('.submit')) {
      callTransfer();
    }
  });

  $("input").keypress(function(event) {
    if (event.which === 13) {
        event.preventDefault();
        callTransfer();
    }
  });
});

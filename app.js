var currencyList = [['USD', 'us'], ['IDR', 'id'], ['BGN', 'bg'], ['ILS', 'il'], ['GBP', 'gb'], ['DKK', 'dk'], ['CAD', 'ca'], ['JPY', 'jp'], ['HUF', 'hu'], ['RON', 'ro'], ['MYR', 'my'], ['SEK', 'se'], ['SGD', 'sg'], ['HKD', 'hk'], ['AUD', 'au'], ['CHF', 'ch'], ['KRW', 'kr'], ['CNY', 'cn'], ['TRY', 'tr'], ['HRK', 'hr'], ['NZD', 'nz'], ['THB', 'th'], ['EUR', 'eu'], ['NOK', 'no'], ['RUB', 'ru'], ['INR', 'in'], ['MXN', 'mx'], ['CZK', 'cz'], ['BRL', 'br'], ['PLN', 'pl'], ['PHP', 'ph'], ['ZAR', 'za']];


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
  $('.loading').css("display", "block");
  $('.third').css("display", "none");
  $('.up_button').css("display", "none");

  $('html, body').animate({
    scrollTop: $('.results').offset().top
  }, 1000);

  var fromCurr = $($('.dropdown')[0]).children()[0].innerText;
  var toCurr = $($('.dropdown')[1]).children()[0].innerText;
  var amount = $('#send_amount')[0].value;

  var baseURL = "http://localhost:5000/getConversion?";
  var fromString = "from_curr=" + fromCurr;
  var toString = "&to_curr=" + toCurr;
  var amountString = "&amount=" + amount;

  var url = baseURL + fromString + toString + amountString;
  $.get(url, function(data) {
    $('.loading').css("display", "none");
    $('.third').css("display", "block");
    $('.up_button').css("display", "block");
    $('.up_button').addClass('animated flipInX');
    for (var i = 0; i < $('.third').length; i++) {
      $($('.third')[i]).addClass('animated flipInX');
    }
    data = JSON.parse(data);
    if (Number(data['finalValue']) === -1) {
      console.log("fake");
      updateResults(amount, getRate(amount - (amount / 10), amount), getRate(0.1, 0.15));
    } else {
      updateResults(amount, Number(data['finalValue']), Number(data['finalRate']));
    }
  });
  // setTimeout(testicle, 4000);
}

function testicle() {
  $('.loading').css("display", "none");
  $('.third').css("display", "block");
  $('.up_button').css("display", "block");
  $('.up_button').addClass('animated flipInX');
  for (var i = 0; i < $('.third').length; i++) {
    $($('.third')[i]).addClass('animated flipInX');
  }
}

function getRate(min, max) {
  return (Math.random() * (max - min + 1)) + min;
}

function updateResults(amount, ourMoney, otherRate) {
  console.log(amount, ourMoney, otherRate);
  if (otherRate > 1) {
    otherRate = getRate(85, 90) / 100;
    console.log("new rate", otherRate);
  }
  otherRate = Math.round(100 * (1 - otherRate));
  ourRate = Math.round(100 * ourRate);
  console.log(amount, ourMoney, otherRate);
  var otherMoney = amount - Math.ceil(amount * (otherRate / 100));
  var ourRate = (amount - ourMoney) / amount;
  var rateDiff = Math.round(Math.abs(otherRate - ourRate));
  var moneyDiff = Math.abs(otherMoney - ourMoney);

  var valList = [otherRate, ourRate, rateDiff, otherMoney, ourMoney, moneyDiff];

  var thirds = $('.third');
  for (var i = 0; i < thirds.length; i++) {
    console.log(valList[i]);
    if (i < 3) {
      valList[i] = valList[i] + '%';
    }
    $(thirds[i]).children()[1].innerText = valList[i];
  }
}

$(document).ready(function() {

  $(window).on('click', function(e) {
    if (e.target.matches('.dropdown') || e.target.matches('.fa-chevron-down')) {
      console.log("up");
      openDropDown(e);
    } else {
      $('.currency_list').css("display", "none");
    }

    if (e.target.matches('.currency')) {
      changeDropDownVal(e);
    }

    if (e.target.matches('.submit') || e.target.matches('.fa-refresh')) {
      callTransfer();
    }

    if (e.target.matches('.up_button') || e.target.matches('.go_up')) {
      $('html, body').animate({
        scrollTop: 0
      }, 1000);
    }
  });

  $("input").keypress(function(event) {
    if (event.which === 13) {
        event.preventDefault();
        callTransfer();
    }
  });
});

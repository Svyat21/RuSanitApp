let payResult = document.querySelector('.pay_result');
let deliveryResult = document.querySelector('.delivery_result');
let trackedPay = document.getElementsByClassName('popup-pay-contain');
let trackedDelivery = document.getElementsByClassName('popup-delivery-contain');

function getPayResult() {
    let payResultChecked = document.querySelector('.popup-pay-contain .jq-radio.checked>input').getAttribute('value');
    if (payResultChecked === 'Наличными') {
        payResult.classList.remove('pay_result_transfer');
        payResult.classList.add('pay_result_cash');
        payResult.querySelector('p').innerHTML = payResultChecked
    } else {
        payResult.classList.remove('pay_result_cash');
        payResult.classList.add('pay_result_transfer');
        payResult.querySelector('p').innerHTML = payResultChecked
    }
}
function getDeliveryResult() {
    let deliveryResultChecked = document.querySelector('.popup-delivery-contain .jq-radio.checked>input').getAttribute('value');
    if (deliveryResultChecked === 'Доставка') {
        deliveryResult.classList.remove('pickup_result_pickup');
        deliveryResult.classList.add('delivery_result_delivery');
        deliveryResult.querySelector('p').innerHTML = deliveryResultChecked
    } else {
        deliveryResult.classList.remove('delivery_result_delivery');
        deliveryResult.classList.add('pickup_result_pickup');
        deliveryResult.querySelector('p').innerHTML = deliveryResultChecked
    }
}

let payWarden = new MutationObserver(function () {
    getPayResult();
});
let deliveryWarden = new MutationObserver(function () {
    getDeliveryResult();
});
if (trackedPay) {
    payWarden.observe(trackedPay.item(0), {childList: true, subtree: true, attributes: true, characterData: true});
    deliveryWarden.observe(trackedDelivery.item(0), {childList: true, subtree: true, attributes: true, characterData: true});
}

$(document).ready(function () {
  $('.small a').click(function(e) {
    if($('.big img').attr('src')!==$(this).attr('href')) {
      $('.big img').hide().attr('src', $(this).attr('href')).fadeIn(200);
    }
    e.preventDefault();
  });
});

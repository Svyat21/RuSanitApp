let minimalPrice = document.querySelector('.content-select').querySelector('.h1-style').innerText;
let minimalPriceInt = Number(minimalPrice.match(/(\d{4,}) руб./)[1]);
let tracked = document.getElementById('form');

function getPrice() {
    let newPrice = 0;
    let selectedPrices = document.querySelectorAll('.jq-selectbox__select-text');
    selectedPrices.forEach(function (el) {
        if (/\d{4,} руб./.test(el.innerText)) {
            newPrice += Number(el.innerText.match(/(\d{4,}) руб./)[1]);
        }
    });
    if (newPrice > minimalPriceInt) {
        document.querySelector('.content-select').querySelector('.h1-style').innerHTML = `${newPrice} руб.`
    } else {
        document.querySelector('.content-select').querySelector('.h1-style').innerHTML = `${minimalPriceInt} руб.`
    }
}

let priceWarden = new MutationObserver(function () {
    getPrice();
});
priceWarden.observe(tracked, {childList: true, subtree: true, characterData: true});

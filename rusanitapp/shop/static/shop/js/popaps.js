document.querySelector('#show_all').addEventListener('click', function (e) {
    let postCount = document.querySelector('#prod_count').getAttribute('count');
    let data = {
        postCount: postCount
    };
    if (document.querySelector('#show_all').classList.value === 'still') {
        document.querySelector('.more').innerHTML = 'Свернуть';
        document.querySelector('#show_all').classList.remove('still');
        document.querySelector('#show_all').classList.add('roll-up');
    } else {
        document.querySelector('.more').innerHTML = 'Показать ещё';
        document.querySelector('#show_all').classList.remove('roll-up');
        document.querySelector('#show_all').classList.add('still');
    }
    $.ajax({
    type: 'GET',
    url: 'show_all/',
    data: data,
    dataType: 'json',
    cache: false,
    success: function (data) {
        let result = data['data']
        document.querySelector('.all-products').innerHTML = '';
        $.each(result, function (key, obj) {
            if (obj['count']) {
                $('.all-products').append(
                    '<div count="' + obj['count'] + '" id="prod_count"></div>'
                );
            } else {
                var tagProduct = '';
                if (obj['tag_product'] === 'hit-of-sales') {
                    tagProduct = '<p class="left-side ' + obj['tag_product'] + '">Хит продаж</p>';
                } else if (obj['tag_product'] === 'new-product') {
                    tagProduct = '<p class="left-side ' + obj['tag_product'] + '">Хит продаж</p>';
                } else {
                    tagProduct = '<p class="left-side"></p>';
                }
                $('.all-products').append(
                    '<div class="card">' +
                        '<div class="card-contain">' +
                            '<div class="upper-part">' +
                                tagProduct +
                                '<div class="right-side">' +
                                    '<p>' + obj['people_amount'] + '</p>' +
                                '</div>' +
                            '</div>' +
                            '<div class="card-photo">' +
                                '<img src="' + obj['main_photo'] + '" alt="#">' +
                            '</div>' +
                            '<p class="text-card-bold">' + obj['name'] + '</p>' +
                            '<p class="text-card">' + obj['short_description'] + '</p>' +
                            '<div class="lower-part">' +
                                '<a href="' + obj['get_absolute_url'] + '" class="button-2">Подробнее</a>' +
                                '<p class="text-card-bold">' + obj['price'] + ' руб.</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>'
                );
            }
        })
    },
    });
    e.preventDefault();
});


const popupLincs = document.querySelectorAll('.popup-link');
const body = document.querySelector('body');
const lockPadding = document.querySelectorAll('.lock-padding');

let unlock = true;

const timeout = 200;

if (popupLincs.length > 0) {
    for (let index = 0; index < popupLincs.length; index++) {
        const popupLink = popupLincs[index];
        popupLink.addEventListener('click', function (e) {
            const popupName = popupLink.getAttribute('href').replace('#', '');
            const curentPopup = document.getElementById(popupName);
            popupOpen(curentPopup);
            e.preventDefault();
        });
    }
}
const popupCloseIcon = document.querySelectorAll('.close-popup');
if (popupCloseIcon.length > 0) {
    for (let index = 0; index < popupCloseIcon.length; index++) {
        const el = popupCloseIcon[index];
        el.addEventListener('click', function (e) {
            popupClose(el.closest('.popup'));
            e.preventDefault();
        });
    }
}

function popupOpen (curentPopup) {
    if (curentPopup && unlock) {
        const popupActive = document.querySelector('.popup.open');
        if (popupActive) {
            popupClose(popupActive, false);
        } else {
            bodyLock();
        }
        curentPopup.classList.add('open');
        curentPopup.addEventListener('click', function (e) {
            if (!e.target.closest('.popup-content')) {
                popupClose(e.target.closest('.popup'));
            }
        });
    }
}
function popupClose(popupActive, doUnlock = true) {
    if (unlock) {
        popupActive.classList.remove('open');
        if (doUnlock) {
            bodyUnLock();
        }
    }
}

function bodyLock() {
    const lockPaddingValue = window.innerWidth - document.querySelector('.main-container').offsetWidth + 'px';

    if (lockPadding.length > 0) {
        for (let index = 0; index < lockPadding.length; index++) {
            const el = lockPadding[index];
            el.style.paddongRight = '0px';
        }
    }
    body.style.paddingRight = lockPaddingValue;
    body.classList.add('lock');

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

function bodyUnLock() {
    setTimeout(function () {
        if (lockPadding.length > 0) {
            for (let index = 0; index < lockPadding.length; index++) {
                const el = lockPadding[index];
                el.style.paddongRight = '0px';
            }
        }
        body.style.paddingRight = '0px';
        body.classList.remove('lock');
    }, timeout);

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

document.addEventListener('keydown', function(e) {
    if (e.which === 27) {
        const popupActive = document.querySelector('.popup.open');
        popupClose(popupActive);
    }
});

document.querySelector('#feedback').addEventListener('click', function (e) {
    $.ajax({
    type: 'GET',
    url: 'feedback/',
    data: {
        'name': $('#name_feedback').val(),
        'phone': $('#phone_feedback').val(),
        'checkbox': $('#checkbox_feedback').val(),
    },
    dataType: 'text',
    cache: false,
    success: false,
    });
    const el = document.querySelector('.close-popup');
    popupClose(el.closest('.popup'));
    e.preventDefault();
})

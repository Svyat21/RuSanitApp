document.getElementById('id_count').value='1';

function valueMinus () {
    let val = document.getElementById('id_count').value;
    if (Number(val) > 0) {
        val = Number(val) - 1;
        document.getElementById('id_count').value=String(val);
    }
}

function valuePlus () {
    let val = document.getElementById('id_count').value;
    if (Number(val) < 10) {
        val = Number(val) + 1;
        document.getElementById('id_count').value=String(val);
    }
}

function specifications () {
    document.querySelector('.specifications').style.display = 'unset';
    document.querySelector('.buttom-specifications').style.color = '#FD9800';
    document.querySelector('.text').style.display = 'none';
    document.querySelector('.buttom-description').style.color = '#2D2D2F';
}

function description () {
    document.querySelector('.specifications').style.display = 'none';
    document.querySelector('.buttom-specifications').style.color = '#2D2D2F';
    document.querySelector('.text').style.display = 'unset';
    document.querySelector('.buttom-description').style.color = '#FD9800';
}
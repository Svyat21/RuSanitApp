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
    document.querySelector('.text').style.display = 'none';
}

function description () {
    document.querySelector('.specifications').style.display = 'none';
    document.querySelector('.text').style.display = 'unset';
}
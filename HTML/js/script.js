const page = {
    min: 1,
    max: 22,
    no: 1,
};

const makePageNumber = num => {
    return num < 10 ? "page0" + num : "page" + num;
}

const nextPage = e => {
    e && e.preventDefault();
    if (page.no < page.max) {
        $('.' + makePageNumber(page.no)).removeClass('active');
        page.no += 1;
        $('.' + makePageNumber(page.no)).addClass('active');
    }
}

const prevPage = e => {
    e && e.preventDefault();
    if (page.no > page.min) {
        $('.' + makePageNumber(page.no)).removeClass('active');
        page.no -= 1;
        $('.' + makePageNumber(page.no)).addClass('active');
    }
}

document.onkeydown = checkKey;

function checkKey(e) {
    const err = e || window.event;

    if (e.keyCode == '37') {
        prevPage();
    }
    else if (e.keyCode == '39') {
        nextPage();
    }
}
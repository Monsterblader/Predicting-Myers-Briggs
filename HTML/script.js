const page = {
    dict: { 1: "page01", 2: "page02", 3: "page03", 4: "page04", 5: "page05", 6: "page06", 7: "page07" },
    min: 1,
    max: 6,
    no: 1,
};

const nextPage = e => {
    e && e.preventDefault();
    if (page.no < page.max) {
        $('.' + page.dict[page.no]).removeClass('active');
        page.no += 1;
        $('.' + page.dict[page.no]).addClass('active');
    }
}

const prevPage = e => {
    e && e.preventDefault();
    if (page.no > page.min) {
        $('.' + page.dict[page.no]).removeClass('active');
        page.no -= 1;
        $('.' + page.dict[page.no]).addClass('active');
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
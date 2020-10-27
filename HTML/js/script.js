const checkKey = e => {
    const err = e || window.event;

    if (e.keyCode == '37') {
        plusSlides(-1);
    }
    else if (e.keyCode == '39') {
        plusSlides(1);
    }
}

// Next/previous controls
const plusSlides = n => {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
const currentSlide = n => {
  showSlides(slideIndex = n);
}

const showSlides = n => {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

let slideIndex = 1;
showSlides(slideIndex);
document.onkeydown = checkKey;

$("button").click(function () {
  $('.predictor')[0].style.display = "none";
  const spinner = $('.spinner')[0].style;
  spinner.display = 'block';
  content = $('textarea')[0].value;
  $.ajax({
    url: "getprediction",
    type: "get",
    data: { content: content },
    success: function (data, status) {
      cats = data.split('');
      spinner.display = "none";
      $('.prediction-result')[0].style.display = 'block';
      setTimeout(() => {
        const EI = $('.EI')[0];
        EI.innerText = cats[0];
        EI.style.display = 'inline';
      }, 1000);
      setTimeout(() => {
        const NS = $('.NS')[0];
        NS.innerText = cats[1];
        NS.style.display = 'inline';
      }, 2000);
      setTimeout(() => {
        const FT = $('.FT')[0];
        FT.innerText = cats[2];
        FT.style.display = 'inline';
      }, 3000);
      setTimeout(() => {
        const JP = $('.JP')[0];
        JP.innerText = cats[3];
        JP.style.display = 'inline';
      }, 5000);
    },
  });
});

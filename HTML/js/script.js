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
const plusSlides = n => showSlides(slideIndex += n);

// Thumbnail image controls
const currentSlide = n => showSlides(slideIndex = n);

const activateTwo = () => {
  setTimeout(() => {
    $('.show-mbti.M, .reveal-wrapper.M').addClass('revealM');
    $('.show-mbti.B, .reveal-wrapper.B').addClass('revealB');
    $('.show-mbti.T, .reveal-wrapper.T').addClass('revealT');
    $('.show-mbti.I, .reveal-wrapper.I').addClass('revealI');
    $('.show-mbti').removeClass('hidden');
  }, 2500);
}

const activateFive = () => {
  setTimeout(() => {
    $('.tool .cat.EI').addClass('rotateOut');
  }, 1500);
  setTimeout(() => {
    $('.tool .cat.EI')[0].innerText = 'I';
    $('.tool .cat.EI').addClass('rotateIn');
    $('.tool .cat.NS').addClass('rotateOut');
  }, 2000);
  setTimeout(() => {
    $('.tool .cat.NS')[0].innerText = 'N';
    $('.tool .cat.NS').addClass('rotateIn');
    $('.tool .cat.FT').addClass('rotateOut');
  }, 2500);
  setTimeout(() => {
    $('.tool .cat.FT')[0].innerText = 'T';
    $('.tool .cat.FT').addClass('rotateIn');
    $('.tool .cat.JP').addClass('rotateOut');
  }, 3000);
  setTimeout(() => {
    $('.tool .cat.JP')[0].innerText = 'P';
    $('.tool .cat.JP').addClass('rotateIn');
  }, 3500);
}

const showSlides = n => {
  const slides = document.getElementsByClassName("mySlides");
  const dots = document.getElementsByClassName("dot");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  switch (n) {
    case 2:
      activateTwo();
      break;
    case 5:
      activateFive();
      break;
  }

  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

const highlightMe = () => {
  const spanStyle = $('.onek')[0].style;
  spanStyle.background = 'rgb(252, 176, 64)';
  spanStyle.color = 'black';
}

$("button").click(function () {
  const getPersonalitySuccess = (data, status) => {
    const thoughts = [];

    for (let i = 0; i < 5; i += 1) {
      thoughts[i] = $('.thought' + (i + 1))[0].style;
    }

    setTimeout(() => {
      thoughts[0].display = 'block';
    }, 1000);
    setTimeout(() => {
      thoughts[0].display = 'none'
      thoughts[1].display = 'block';
    }, 2000);
    setTimeout(() => {
      thoughts[1].display = 'none';
      thoughts[2].display = 'block';
    }, 3000);
    setTimeout(() => {
      thoughts[2].display = 'none';
      thoughts[3].display = 'block';
    }, 4000);
    setTimeout(() => {
      document.getElementsByTagName('audio')[0].play();
      thoughts[3].display = 'none';
      thoughts[4].display = 'block';
    }, 5000);

    setTimeout(() => {
      const makeTimeouts = (cats) => {
        const pair_names = ['EI', 'NS', 'FT', 'JP'];
        const pairs = [];

        for (let i = 0; i < pair_names.length; i += 1) {
          pairs[i] = $('.prediction-result .' + pair_names[i])[0];
        }

        for (let i = 0; i < pair_names.length; i += 1) {
          setTimeout(() => {
            pairs[i].innerText = cats[i];
            pairs[i].style.display = 'inline';
          }, i * 1000);
        }
      }

      spinner.display = "none";
      $('.thinking')[0].style.display = 'none';
      $('.prediction-result')[0].style.display = 'block';

      makeTimeouts(data.split(''));
    }, 8000);
  }
  const spinner = $('.spinner')[0].style;
  const content = $('textarea')[0].value;

  $('.predictor')[0].style.display = "none";
  spinner.display = 'block';
  $.ajax({
    url: "getprediction",
    type: "get",
    data: { content },
    success: getPersonalitySuccess,
  });
});

let slideIndex = 1;

showSlides(slideIndex);
document.onkeydown = checkKey;

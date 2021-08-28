$(document).ready(function () {
  $('.small a').click(function(e) {
    if($('.big img').attr('src')!==$(this).attr('href')) {
      $('.big img').hide().attr('src', $(this).attr('href')).fadeIn(200);
    }
    e.preventDefault();
  });
});
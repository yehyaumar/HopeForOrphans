jQuery(document).ready(function($)
{

  $(".accordian").on("click", ".card-div", function () {
      $(this).toggleClass("active").next().slideToggle();
  })
});
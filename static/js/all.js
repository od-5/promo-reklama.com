$(document).ready(function () {

  // fancybox
  jQuery('.fancybox').fancybox();
  // popup close
  $(document).on('click','.popup-close',function(e){
    e.preventDefault();
    $.fancybox.close();
  });

  $(".input[name='phone']").mask("+7 (999) 999-99-99");
  $('.js-ticket-form').each(function(){
    $(this).validate({
         rules: {
        name: {
          required: true,
          minlength: 3
        },
        phone: {
          required: true,
          minlength: 3
        },
        mail: {
          required: true,
          email: true
        }
      }
    });
		$(this).submit(function(e) {
			console.log($(this));
			if ($(this).find('input[name=city]').val() == '') {
				e.preventDefault();
				$('.city-link').trigger('click');
			}
		});
  });
	$('.js-ticket-form').ajaxForm({
      success: function(data){
        if (data.success) {
            location.replace("/thnx/");
        }
        $('.js-ticket-form').trigger('reset');
      }
  });
  // fake-select hidden
  $(document).on('click', '.city-region-link', function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $('.city-region-block').slideUp();
      $(this).removeClass('active');
    }else{
      $('.city-region-block').slideDown();
      $(this).addClass('active');
    }
  });
  $(document).bind( "mouseup touchend", function(e){
    var container = $('.fake-select-hidden, .fake-select-link');
    if (!container.is(e.target) // if the target of the click isn't the container...
      && container.has(e.target).length === 0) // ... nor a descendant of the container
    {
      $('.fake-select-hidden').slideUp();
      $('.fake-select-link').removeClass('active');
    }
  });

  // button info
  $(document).on('click','.button-data',function(e){
    e.preventDefault();
    var data_title = $(this).attr('data-title');
    var data_theme = $(this).attr('data-theme');
    $('#popup input[name=theme]').val(data_theme);
    $('#popup .insert-title').text(data_title);
  });

  // slider
  $('.review-slider .owl-carousel').owlCarousel({
    loop: true,
    items: 1,
    nav: true,
    dots: false,
    //autoHeight : true,
    navText: [''],
    autoplay: false
  });


  //  ввод города
  $('.input_city').each(function(){
    $(this).autocomplete({
      source: function(request, response){
        // организуем кроссдоменный запрос
        $.ajax({
          url: $('.input_city').data('url'),
          dataType: "json",
          // параметры запроса, передаваемые на сервер (последний - подстрока для поиска):
          data:{
            style: "full",
            maxRows: 12,
            name_startsWith: request.term
          },
          // обработка успешного выполнения запроса
          success: function(data){
            console.log(data);
            if(data.city_list.length){
              console.log('OK');
              $('.city-input-text').hide();
            }else {
              console.log('nothing');
              $('.city-input-text').show();
            }
            // приведем полученные данные к необходимому формату и передадим в предоставленную функцию response
            response($.map(data.city_list, function(item){
              return{
                label: item.name,
                value: item.name
              }
            }));
          }
        });
      },
      minLength: 2
    });
  });

});



let intro = document.querySelector('.introPagina');
let logo = document.querySelector('.logo');
let logoSpan = document.querySelectorAll('.logo-parts');

window.addEventListener('DOMContentLoaded', () => {



    let ubicacionPrincipal = window.pageYOffset;
    window.onscroll = function (){
    let DesplazamientoActual = window.pageYOffset;
    if(ubicacionPrincipal >= DesplazamientoActual) {
        document.getElementById("navbar").style.top = "0";
        document.getElementById("navbar2").style.top = "0";
        document.getElementById("navbar2").style.position = "relative";
     
    }
    else{
        document.getElementById("navbar").style.top = "-100px";
        document.getElementById("navbar2").style.top = "-100px";
    }
    ubicacionPrincipal = DesplazamientoActual;
 }

 $('.boxInputLogin input').focus(function(){
    $('.rayaBottomLogin').css({//O lo que desees
      "height": "100%", //O lo que desees
      "background-color": "rgb(245, 210, 12)"
    });
  });
  $('.boxInputLogin input').focusout(function(){
    $('.rayaBottomLogin').css({//O lo que desees
      "background-color": "transparent",
      "height": "2%" ,//O lo que desees
    });
  });
  



    $('.filtrados .categoriaItem[category="todo"]').addClass('ctItemActive');
    

    $('.categoriaItem').click(function () {
        var catProducto = $(this).attr('category');

        $('.categoriaItem').removeClass('ctItemActive');
        $(this).addClass('ctItemActive');

        //ocualtaodno productos

        //$('.cardCAJA').css('transform', 'scale(0)');
        $('.card-border').css('margin-top', '100px');
        $('.cardCAJA').css('opacity', '0');
        function hideProduct(){
            $('.cardCAJA').hide();
        }setTimeout(hideProduct,300)


        //mostradno productospos
        function showProduct(){
            $('.cardCAJA[category="'+catProducto+'"]').show();
            $('.cardCAJA[category="'+catProducto+'"]').css('opacity', '1');
            $('.card-border').css('margin-top', '0px');
            //$('.cardCAJA[category="'+catProducto+'"]').css('transform','scale(1)');
        }setTimeout(showProduct,300)
    });

    $('.categoriaItem[category="todo"]').click(function () {
        
        function showAllProduct(){
            $('.card-border').css('margin-top', '100px');
            $('.cardCAJA').show();
            //$('.cardCAJA').css('transform','scale(1)');
            $('.card-border').css('margin-top', '0px');
            $('.cardCAJA').css('opacity', '1');
        }setTimeout(showAllProduct,300)
    });



    //FILTRO PRECIOS
	$(".botonFiltroCosto").click(function () { 
        var valorMINIMO = (Number($(".input-min-PRECIO").val()));
        var valorMAXIMO = (Number($(".input-max-PRECIO").val()));
        if (valorMAXIMO == 0){
            valorMAXIMO = 10000000 
        }
        //HIDE PRODUCTOS
        $('.card-border').css('margin-top', '100px');
        $('.cardCAJA').css('opacity', '0');
        function hideProductPrice(){
            $('.cardCAJA').hide();
        }setTimeout(hideProductPrice,300)

        $('.cardCAJA').each(function (){
            let precio = Number($(this).attr('price'))

            if (valorMINIMO <= precio && precio <= valorMAXIMO){


            function showProductPrice(){
                $('.cardCAJA[price="'+(precio).toFixed(2)+'"]').show();
                $('.cardCAJA[price="'+(precio).toFixed(2)+'"]').css('opacity', '1');
                $('.card-border').css('margin-top', '0px');
                //$('.cardCAJA[category="'+catProducto+'"]').css('transform','scale(1)');
            }setTimeout(showProductPrice,300)

        
            }     
        })
        });	





    if( !localStorage.getItem('ingreso') ){
        intro.style.display = 'flex';
        setTimeout(() => {

            logoSpan.forEach((span, index)=>{
                setTimeout(() => {
                    span.classList.add('active')
                }, (index+1)*120);
            })
    
    
            setTimeout(() => {
    
                logoSpan.forEach((span,index) => {
                    setTimeout(() => {
                        span.classList.remove('active')
                        span.classList.add('fade')
                    }, (span + 1 ) * 50);
                })
            }, 3000);
    
            setTimeout(() => {
                intro.style.opacity = '0';
                intro.style.top = '-100vh';
            }, 3300);

            localStorage.setItem('ingreso',1); 
    
    
        
        });
    
    } 
    else {
        intro.style.display = 'none';
        localStorage.setItem('ingreso',1); 
        let a = localStorage.getItem("ingreso");
        console.log(a);
        let contador = Number(a);
        localStorage.setItem('ingreso',++contador);
    }














});









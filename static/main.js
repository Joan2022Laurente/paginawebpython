
let intro = document.querySelector('.introPagina');
let logo = document.querySelector('.logo');
let logoSpan = document.querySelectorAll('.logo-parts');

window.addEventListener('DOMContentLoaded', () => {

    $('.filtrados .categoriaItem[category="todo"]').addClass('ctItemActive');
    

    $('.categoriaItem').click(function () {
        var catProducto = $(this).attr('category');

        $('.categoriaItem').removeClass('ctItemActive');
        $(this).addClass('ctItemActive');

        //ocualtaodno productos
        $('.cardCAJA').hide();
        //mostradno productos
        $('.cardCAJA[category="'+catProducto+'"]').show();
    });

    $('.categoriaItem[category="todo"]').click(function () {

        $('.cardCAJA').show();
    });

    //PRECIOSSSSSS

	$(".botonFiltroCosto").click(function () {
        var valorMINIMO = (Number($(".input-min-PRECIO").val()));
        var valorMAXIMO = (Number($(".input-max-PRECIO").val()));
        console.log(valorMAXIMO, valorMINIMO)
        //ocualtaodno productos
        $('.cardCAJA').hide();
        $('.cardCAJA').each(function (){
            let precio = Number($(this).attr('price'))
            if (valorMINIMO <= precio && precio <= valorMAXIMO){

            $('.cardCAJA[price="'+(precio).toFixed(2)+'"]').show();
            console.log(precio)
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










    let ubicacionPrincipal = window.pageYOffset;
window.onscroll = function (){
    let DesplazamientoActual = window.pageYOffset;
    if(ubicacionPrincipal >= DesplazamientoActual) {
        document.getElementById("navbar").style.top = "0";
     
    }
    else{
        document.getElementById("navbar").style.top = "-100px";
    }
    ubicacionPrincipal = DesplazamientoActual;
}



});








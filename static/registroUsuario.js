

	$('#signupSubmit').on('click', function(e) { //CLICK EN EL BOTON
		e.preventDefault();
		var name = $('#fullname').val();
		var email = $('#email').val();
		var pwd = $('#password').val();
		var cnfpwd = $('#cnfpassword').val();
		
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;

		if(email != "" && pwd != "" && cnfpwd != "") {
			if(pwd != cnfpwd) {
				$('#msg').html('<span style="color: red;">LAS CONTRASEÑAS NO COINCIDEN</span>');
			} else if(!regex.test(email)) {
				$('#msg').html('<span style="color: red;">CORREO INVALIDO</span>');
			} else {
				$.ajax({
					method: "POST",
					url: '/registroNewUser',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'name': name, 'email': email, 'password': pwd}),
					dataType: "json",
					success: function(response) {
						localStorage.setItem('loggedin', 1,);
						var datosDelUser = JSON.stringify(response)
						var datitos = JSON.parse(datosDelUser);
						localStorage.setItem('usuarioNOMBRE',datitos[0]["datos"]["nombre"])
						localStorage.setItem('usuarioCORREO',datitos[0]["datos"]["correo"])
						document.getElementById("nombreDelUser").innerHTML =  localStorage.usuarioNOMBRE
						$('#msglog').html('<span style="color: green;">Hola de nuevo '+ localStorage.usuarioNOMBRE +'</span>');
						$('#liNombreUser').css("display", "flex");
						$('#logoutBOTON').css("display", "flex");
						$("#inicioSESION").hide();
						
						// localStorage.setItem('loggedin', 1,);
						// document.getElementById("nombreDelUser").innerHTML =  localStorage.usuarioNOMBRE
						// $('#liNombreUser').css("display", "flex");
						// $('#logoutBOTON').css("display", "flex");
						// $("#inicioSESION").hide();
						// $('#msg').html('<span style="color: green;">USUARIO REGISTRADO CORRECTAMENTE</span>');
					},statusCode: {
						400: function() {
							$('#msg').html('<span style="color: red;">NO RELLENASTE TODOS LOS PARAMETROS</span>');
						},
						409 : function() {
							$('#msg').html('<span style="color: red;">YA ESTAS REGISTRADO</span>');
						}
					},
					error: function(err) {
						console.log(err);
					}
				});
			}
		} else {
			$('#msg').html('<span style="color: red;">NO RELLENASTE TODOS LOS PARAMETROS</span>');
		}
	});



	var isLoggedIn = localStorage.getItem('loggedin');
	
	if(isLoggedIn == 1) {
		document.getElementById("nombreDelUser").innerHTML =  localStorage.usuarioNOMBRE
		$('#logoutBOTON').css("display", "flex");
		$('#liNombreUser').css("display", "flex");		
		$("#inicioSESION").hide();
	} else {
		$('#logoutBOTON').hide();
		$('#liNombreUser').hide();		
		$("#inicioSESION").css("display", "flex");

	}
	
	$('#loginSubmit').on('click', function(e) {
		e.preventDefault();
		
		var email = $('#emailLogin').val();
		var pwd = $('#passwordLogin').val();
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		if(email != "" && pwd != "" ) {
			if(!regex.test(email)) {
				$('#msglog').html('<span style="color: red;">Correo invalido</span>');
			} else {
				$.ajax({
					method: "POST",
					url: '/loginUSER',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'username': email, 'password': pwd}),
					dataType: "json",
					success: function(response) {
						localStorage.setItem('loggedin', 1,);
						var datosDelUser = JSON.stringify(response)
						var datitos = JSON.parse(datosDelUser);
						localStorage.setItem('usuarioCORREO', datitos[0]["datos"]["correo"])
						localStorage.setItem('usuarioNOMBRE',datitos[0]["datos"]["nombre"])
						document.getElementById("nombreDelUser").innerHTML =  localStorage.usuarioNOMBRE
						$('#msglog').html('<span style="color: green;">Hola de nuevo '+ localStorage.usuarioNOMBRE +'</span>');
						$('#liNombreUser').css("display", "flex");
						$('#logoutBOTON').css("display", "flex");
						$("#inicioSESION").hide();
					},
					statusCode: {
						400: function() {
							$('#msglog').html('<span style="color: red;">Bad request - invalid credentials</span>');
                            localStorage.setItem('usuario',user)
						}
					},
					error: function(err) {
                        localStorage.setItem('usuario',err)
						console.log(err);
					}
				});
			}
		} else {
			$('#msglog').html('<span style="color: red;">Invalid username and password</span>');
		}
	});
	
	$('#logoutBOTON').on('click', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: '/logout',
			dataType: "json",
			success: function(data) {
				$('#msglog').html('<span></span>');
				localStorage.setItem('loggedin', 0);
				$("#inicioSESION").css("display", "flex");
				$('#logoutBOTON').hide();
				$('#liNombreUser').hide();
			},
			error: function(err) {
				console.log(err);
			}
		});
	});

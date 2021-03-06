$(document).ready(function() {

	$("#menu-icon").click(function(e) {
		$("#menu-div").css("display", "block");
		$("#menu-icon").css("display", "none");
		$("#menu-close").css("display", "block");
		$("#outer-container").css("display", "none");
    });

  $("#menu-close").click(function(e) {
		$("#menu-div").css("display", "none");
		$("#menu-icon").css("display", "block");
		$("#menu-close").css("display", "none");
		$("#outer-container").css("display", "block");
		});

	  // Check for click events on the navbar burger icon
	  $(".navbar-burger").click(function() {
		// Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
		$(".navbar-burger").toggleClass("is-active");
		$(".navbar-menu").toggleClass("is-active");
  
	});

		
	function initialiseCookieConsent() {
		window.cookieconsent.initialise({
			domain: "jurisprudencia.pt",
			"palette": {
				"popup": {
					"background": "#e3e5e4",
					"text": "#3c434f"
				},
				"button": {
					"background": "#b4dce0",
					"text": "#3c434f"
				}
			},
			"content": {
				"message": "Este website usa cookies para melhorar o site e a sua experiência.",
				//"allow": "OK, pode ser",
				"dismiss": "OK",
				"link": "Saiba mais",
				"href": "/termos"
			},
			//"type": "opt-in",
		});
	}

	initialiseCookieConsent();
	enableGa();

	function restartCookieConsent() {
		deleteCookie("cookieconsent_status");
		initialiseCookieConsent();
	}

	function enableGa() {
		// only activate ga if not on localhost
		if (document.location.hostname.search("jurisprudencia.pt") !== -1) {
			window.dataLayer = window.dataLayer || [];
			function gtag(){dataLayer.push(arguments);}
			gtag('js', new Date());

			gtag('config', 'UA-116554949-1');
		}
	}

	function disableGa() {
		var a = document.location.hostname;
		deleteJurisCookie("_ga");
		deleteJurisCookie("_gat_gtag_UA_116554949_1");
		deleteJurisCookie("_gid");
	}

	$("#cookieBtn").click(function(e) {
		restartCookieConsent();
	});

	function deleteCookie(name) {
		document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
	}

	function deleteJurisCookie(name) {
		var domain;
		if (document.location.hostname.search("jurisprudencia.pt") !== -1) {
			domain = ".jurisprudencia.pt";
		}	
		else {
			domain = "127.0.0.1";
		}
		document.cookie = name +'=; Path=/; Domain=' + domain + '; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
	}

	function getCookie(name) {
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++) {
				var c = ca[i];
				while (c.charAt(0)==' ') c = c.substring(1,c.length);
				if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
		}
		return null;
	}	

});
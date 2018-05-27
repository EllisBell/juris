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

		
	function initialiseCookieConsent() {
		window.cookieconsent.initialise({
			domain: "jurisprudencia.pt",
			revokable: false,
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
				"message": "Este website usa cookies para melhorar o site e a sua experiência. OK?",
				"allow": "OK, pode ser",
				"dismiss": "Não obrigado",
				"link": "Saiba mais",
				"href": "/termos"
			},
			"type": "opt-in",
			onInitialise: function(status) {
				var type = this.options.type;
				if(type == 'opt-in' && status== "allow") {
					enableGa();
				}
			},
			onStatusChange: function(status, chosenBefore) {
				if(status == "allow") {
					enableGa();
				}
				if(status == "dismiss") {
					disableGa();
				}
				location.reload();
			},
		});
	}

	// if user has ga cookie there already but cookie consent is not allow,
	// ask for consent again
	if(getCookie("_ga") && getCookie("cookieconsent_status") != "allow") {
		restartCookieConsent();
	};

	initialiseCookieConsent();

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
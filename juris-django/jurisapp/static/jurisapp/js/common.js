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
			domain: ".jurisprudencia.pt",
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
				"dismiss": "Nao obrigado",
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

	initialiseCookieConsent();

	$("#cookieBtn").click(function(e) {
		delete_cookie("cookieconsent_status");
		initialiseCookieConsent();
	});

	function delete_cookie(name) {
		document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
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
		delete_cookie("_ga");
		delete_cookie("_gat_gtag_UA_116554949_1");
		delete_cookie("_gid");
	}

});
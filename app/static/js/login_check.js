document.addEventListener('DOMContentLoaded', function() { 
    var loginButton = document.getElementById('login-button'); 
    if (loginButton) { 
        loginButton.addEventListener('click', function(event) { 
            event.preventDefault(); 

            var login = document.getElementById('username').value; 
            var password = document.getElementById('password').value; 

            var xhr = new XMLHttpRequest(); 
            xhr.open('POST', '/doctor/search'); // Изменено на '/doctor/search'
            xhr.setRequestHeader('Content-Type', 'application/json'); 
            xhr.onload = function() { 
                if (xhr.status === 200) { 
                    var doctor = JSON.parse(xhr.responseText); 
                    window.location.href = '/donor/list'; 
                } else if (xhr.status === 404) { 
                    alert('Doctor not found.'); 
                } else { 
                    alert('An error occurred.'); 
                } 
            }; 
            xhr.send(JSON.stringify({ 
                'login': login, 
                'password': password 
            })); 
        }); 
    } 
});
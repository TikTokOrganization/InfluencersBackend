const googleAuthHandler = google.accounts.oauth2.initCodeClient({
    client_id: '620677125812-g4634rpb7kam1r5hm8kq2mdccdhg3i5l.apps.googleusercontent.com',
    scope: 'https://www.googleapis.com/auth/youtube',
    ux_mode: 'popup',
    callback: (response) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', "http://localhost:8080/login", true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        // Set custom header for CRSF
        xhr.setRequestHeader('X-Requested-With', 'XmlHttpRequest');
        xhr.onload = function() {
            console.log('Auth code response: ' + xhr.responseText);
            window.location.replace("http://localhost:8080/oauth2callback");
        };
        xhr.send('code=' + response.code);
    }
});
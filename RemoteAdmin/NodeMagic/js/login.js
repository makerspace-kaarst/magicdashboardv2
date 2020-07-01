function login() {
    SERVER = document.getElementById('login-ip')
        .value;
    if (!SERVER.startsWith('http://')) {
        SERVER = 'http://' + SERVER;
    }
    PORT = document.getElementById('login-port')
        .value;
    PASSWORD = document.getElementById('login-key')
        .value;
    document.getElementById('login-main')
        .style = 'display:none';
    document.getElementById('app-main')
        .style = '';

    document.getElementById('form-password')
        .value = PASSWORD;
    // Bootup update
    updateContext();
}

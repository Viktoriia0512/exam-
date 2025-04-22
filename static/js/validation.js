function togglePassword(id, el) {
    var x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
        el.textContent = "🙈";
    } else {
        x.type = "password";
        el.textContent = "🐵";
    }
}

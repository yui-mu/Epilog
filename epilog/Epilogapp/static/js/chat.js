// static/js/chat.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function (event) {
            console.log("送信ボタンが押されました");
        });
    }
});

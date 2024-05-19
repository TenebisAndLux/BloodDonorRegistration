function showLogoutButton() {
    document.querySelector(".exit-button").style.display = "block";
}

function hideLogoutButton() {
    setTimeout(function () {
        if (!document.querySelector(".name-container:hover") && !document.querySelector(".exit-button:hover")) {
            document.querySelector(".exit-button").style.display = "none";
        }
    }, 500);
}

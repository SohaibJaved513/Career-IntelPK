document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".feature, .panel, .job-card, .mini-stat, .glass-card");

    cards.forEach(function (card) {
        card.addEventListener("mouseenter", function () {
            card.style.boxShadow = "0 24px 70px rgba(53, 211, 255, 0.09)";
        });

        card.addEventListener("mouseleave", function () {
            card.style.boxShadow = "";
        });
    });
});

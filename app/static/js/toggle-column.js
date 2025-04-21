
function toggleColumn(columnClass) {
    const elements = document.querySelectorAll(`.${columnClass}`);
    elements.forEach(element => {
        if (element.style.display === "none") {
            element.style.display = "";
        } else {
            element.style.display = "none";
        }
    });
}

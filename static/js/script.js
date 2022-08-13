document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('copyright-year').innerHTML = new Date().getFullYear();

    if(document.URL.includes("contact")){
        document.getElementById("contact-header").scrollIntoView();
    }

    if(document.URL.includes("contact") || document.URL.includes("home")){
        scrollSpy();
    }

    if(document.getElementById("button-id-edit")) {
        document.addEventListener("click", enableFields)
    }
});

setTimeout(function() {
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);

function enableFields() {
    inputs = document.querySelectorAll(".form-control, .form-select");
    console.log(inputs)
    for(input of inputs){
        input.removeAttribute('disabled');
    }
};

// Code taken from https://medium.com/p1xts-blog/scrollspy-with-just-javascript-3131c114abdc by P1xt
function scrollSpy(){
    // Get relevant sections as a Nodelist
    const sections = document.querySelectorAll(".scrollspy");
    // Get relevant links as a Nodelist
    const nav_links = document.querySelectorAll(".scrollspy-link");


    // Accesses the nav_links Nodelist using a passed in index to add the active class
    const makeActive = (link) => nav_links[link].classList.add("active");
    // Accesses the nav_links Nodelist using a passed in index to remove the active class
    const removeActive = (link) => nav_links[link].classList.remove("active");
    // Creates a new array using the length of sections and calling the .keys() method on this
    // which creates an array of indexes (i.e. [0, 1, 2, ...]), each of these is then passed to removeActive
    const removeAllActive = () => [...Array(sections.length).keys()].forEach((link) => removeActive(link));

    // Variable used in the calculation of when a section is classed as "in view", reduces how close
    // the section needs to be to the top
    const sectionMargin = 400;

    // Track the currently active link
    let currentActive = 0;

    window.addEventListener("scroll", () => {

        // Find the index for the currently in view section by comparing the section's offsetTop value to the current viewport position
        // Sections are checked in reverse order otherwise findIndex would always return the first element
        const current = sections.length - [...sections].reverse().findIndex((section) => window.scrollY >= section.offsetTop - sectionMargin) - 1

        // If section changes then remove active classes and add active class to the current link
        if (current !== currentActive) {
            removeAllActive();
            currentActive = current;
            makeActive(current);
        }
    });    
}
// End of code taken from https://medium.com/p1xts-blog/scrollspy-with-just-javascript-3131c114abdc by P1xt


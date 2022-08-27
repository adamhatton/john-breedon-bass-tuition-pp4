const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'), {
    backdrop: 'static',
    keyboard: false
});
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalConfirmBtn = document.getElementById("modal-confirm-btn");

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('copyright-year').innerHTML = new Date().getFullYear();

    // Scroll to contact section if user has selected contact navlink
    if(document.URL.includes("contact")){
        document.getElementById("contact-header").scrollIntoView();
    }

    // Attach the scrollSpy if user is on Home or Contact page
    if(document.URL.includes("contact") || document.URL.includes("home")){
        scrollSpy();
    }

    // Add listener to the profile edit button
    if(document.getElementById("button-id-edit")) {
        document.getElementById("button-id-edit").addEventListener("click", toggleFieldsDisabled);
    }

    // Add listener to the cancel profile edit button
    if(document.getElementById("button-id-cancel")) {
        document.getElementById("button-id-cancel").addEventListener("click", toggleFieldsDisabled);
    }

    // Add listener to the add testimonial button 
    if(document.getElementById("add-testimonial-btn")) {
        let addTestButton = document.getElementById("add-testimonial-btn");
        let addTestForm = document.getElementById("add-testimonial-form");

        // Toggle the testimonial form
        addTestButton.addEventListener("click", () => {
            if (addTestForm.classList.contains("hidden")) {
                addTestForm.classList.remove("hidden");
                addTestButton.innerHTML = "Hide";
            } else {
                addTestForm.classList.add("hidden");
                addTestButton.innerHTML = "Add Testimonial";
            }
        });
    }

    // Add listener to the delete testimonial button
    if(document.getElementById("testimonial-delete-btn")) {
        document.getElementById("testimonial-delete-btn").addEventListener("click", function(){ 
            confirmDelete('learner_account/delete_testimonial/', 'testimonial');
    });
    }

    // Get all delete booking buttons
    let delBtns = document.getElementsByClassName("del-booking-btn");
    if (delBtns) {
        // Add listeners to each of the delete booking buttons so that they will trigger the confirmDelete function
        for (let btn of delBtns) {
            let urlId = btn.dataset.bookingId;
            btn.addEventListener("click", function() {
                confirmDelete(`bookings/delete_booking/${urlId}/`, 'booking');
            });
        }
    }

    // Get all the available booking slot buttons
    let slotBtns = document.getElementsByClassName("booking-free");
    if (slotBtns) {
        // Add listeners to each of the available slot buttons
        for (let btn of slotBtns) {
            btn.addEventListener("click", populateBookingForm);
        }
    }
});

setTimeout(function() {
    // Clear messages after 3 seconds
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);

/**
 * 
 * Opens a confirmation modal, sets the text, and attaches a form submit
 * function to the confirm button
 */
function confirmForm(formName) {
    confirmModal.show();
    let title = document.querySelector(".modal-title");
    let body = document.querySelector(".modal-body");
    title.innerHTML = "Confirm submission";
    body.innerHTML = "Would you like to submit this form?";
    let form = document.getElementById(formName);

    let confirmAction = function() {
        form.submit();
        confirmModal.hide();
        modalConfirmBtn.removeEventListener("click", confirmAction);
    };

    modalConfirmBtn.addEventListener("click", confirmAction);

    // Remove the submit listener if user closes modal
    modalCloseBtn.addEventListener("click", () => {
        modalConfirmBtn.removeEventListener("click", confirmAction);
    });
}

/**
 * 
 * Opens a confirmation modal, sets the text, and attaches a redirect to
 * a url for deleting testimonials
 */
function confirmDelete(redirectUrl, delItem) {
    confirmModal.show();
    let title = document.querySelector(".modal-title");
    let body = document.querySelector(".modal-body");
    title.innerHTML = "Confirm deletion";
    body.innerHTML = `Would you like to delete this ${delItem}?`;

    let confirmAction = function() {
        window.location.pathname = redirectUrl;
    };

    modalConfirmBtn.addEventListener("click", confirmAction);

    // Remove the submit listener if user closes modal
    modalCloseBtn.addEventListener("click", () => {
        modalConfirmBtn.removeEventListener("click", confirmAction);
    });
}

/**
 * Uses the booking slot information to pre-populate the booking form
 */
function populateBookingForm() {
    let bookingForm = document.getElementById('bookings-form').elements;
    let dateField = bookingForm.id_date;
    let timeField = bookingForm.id_time;
    let time = this.innerHTML.slice(0,2);
    let date = getSlotDate(this);
    timeField.value = time;
    dateField.value = date.dataset.dateStr;
}

/**
 * Takes a booking button and finds the previous h3 element
 */
function getSlotDate(slot){
    let element = slot.previousElementSibling;
    while (true) {
        if (element.tagName == 'H3') return element;
        element = element.previousElementSibling;
    }
}

/**
 * Toggles the disabled state of the fields in the profile information form
 */
function toggleFieldsDisabled() {
    // Create variables for the different elements to disable
    let inputs = document.querySelectorAll(".form-control, .form-select");
    let cancelBtn = document.getElementById("button-id-cancel");
    let submitBtn = document.getElementById("submit-id-submit");
    let editBtn = document.getElementById("button-id-edit");
    let helpText = document.getElementById("hint_id_username");

    // When edit is pressed the disabled state is removed from inputs and Submit
    // When cancel is pressed the disabled state is reapplied
    if (this.id == "button-id-edit") {
        for(let input of inputs){
            input.removeAttribute('disabled');
        }
        cancelBtn.classList.remove("hidden");
        submitBtn.removeAttribute('disabled');
        helpText.style.display = "block";
    } else if (this.id == "button-id-cancel") {
        for(let input of inputs){
            input.setAttribute('disabled', '');
        }
        editBtn.classList.remove("hidden");
        submitBtn.setAttribute('disabled', '');
        helpText.style.display = "none";
    }

    this.classList.add("hidden");
}

// Code taken from https://medium.com/p1xts-blog/scrollspy-with-just-javascript-3131c114abdc by P1xt
function scrollSpy(){
    // Get relevant sections as a Nodelist
    const sections = document.querySelectorAll(".scrollspy");
    // Get relevant links as a Nodelist
    const navLinks = document.querySelectorAll(".scrollspy-link");


    // Accesses the nav_links Nodelist using a passed in index to add the active class
    const makeActive = (link) => navLinks[link].classList.add("active");
    // Accesses the nav_links Nodelist using a passed in index to remove the active class
    const removeActive = (link) => navLinks[link].classList.remove("active");
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
        const current = sections.length - [...sections].reverse().findIndex((section) => window.scrollY >= section.offsetTop - sectionMargin) - 1;

        // If section changes then remove active classes and add active class to the current link
        if (current !== currentActive) {
            removeAllActive();
            currentActive = current;
            makeActive(current);
        }
    });    
}
// End of code taken from https://medium.com/p1xts-blog/scrollspy-with-just-javascript-3131c114abdc by P1xt


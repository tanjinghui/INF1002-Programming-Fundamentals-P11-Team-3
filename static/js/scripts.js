// Scripts
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


window.validateForm = function() {
    return checkValidation();
}

function checkValidation() {
    let valid = true;

    const startError = document.getElementById("start_error");
    const endError = document.getElementById("end_error");
    const windowError = document.getElementById("window_error");

    // Clear previous error messages
    if (startError) startError.textContent = "";
    if (endError) endError.textContent = "";
    if (windowError) {
        windowError.textContent = "";
        windowError.style.display = "none";
    }

    // Get input values
    const startInput = document.getElementById("start_date");
    const endInput = document.getElementById("end_date");
    const windowInput = document.getElementById("days_window");

    const startVal = startInput?.value || null;
    const endVal = endInput?.value || null;
    const windowVal = windowInput?.value || null;

    // Validate days window
    const start = startVal ? new Date(startVal) : null;
    const end = endVal ? new Date(endVal) : null;
    const daysWindow = windowVal ? parseInt(windowVal) : null;

    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set to start of day

    // Invalid date format
    if (startVal && isNaN(start.getTime())) {
        startError.textContent = "Please select a valid start date.";
        valid = false;
    }

    if (endVal && isNaN(end.getTime())) {
        endError.textContent = "Please select a valid end date.";
        valid = false;
    }

    // End date must be after start date
    if (start && end && start > end) {
        endError.textContent = "End date must be after start date.";
        valid = false;
    }

    // Prevent dates beyond today (future dates)
    if (start && start > today) {
        startError.textContent = "Start date cannot be in the future.";
        valid = false;
    }

    if (end && end > today) {
        endError.textContent = "End date cannot be in the future.";
        valid = false;
    }
    // Validate days window
    if (daysWindow !== null && windowError) {
        if (daysWindow < 1 || isNaN(daysWindow)) {
            windowError.textContent = "Window must be at least 1 day.";
            valid = false;
        } else if (start && end && daysWindow > Math.ceil((end - start) / (1000*60*60*24))) {
            windowError.textContent = "Window cannot exceed total days in range (" + Math.ceil((end - start)/(1000*60*60*24)) + ").";
            valid = false;
        }
    }

    // Prevent dates that are too big (e.g., year 9999)
    const maxAllowedYear = 2025;
    if (start && start.getFullYear() > maxAllowedYear) {
        startError.textContent = `Start date cannot be after year ${maxAllowedYear}.`;
        valid = false;
    }

    if (end && end.getFullYear() > maxAllowedYear) {
        endError.textContent = `End date cannot be after year ${maxAllowedYear}.`;
        valid = false;
    }

    return valid;
}

document.addEventListener("DOMContentLoaded", function () {
    ["start_date", "end_date", "days_window"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener("input", checkValidation);
    });
});
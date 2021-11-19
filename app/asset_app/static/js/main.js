// general funtion to get element
const getElement = (selector) => {
    const element = document.querySelector(selector);
    if (element) return element
    else return null

}

// show/hide left nav bar
const showMenu = () => {

    const element = getElement(".side-nav-bar");
    element.classList.toggle("show-side-nav-bar");
}
const navBtn = getElement(".nav-btn");

if (navBtn) {
    navBtn.addEventListener('click', showMenu);
}


// close the flash messages modal
let closeButtonBottom = document.getElementById('close');
const hideModal = () => {

    const modal = getElement(".modal")
    modal.style.display = "none";
}

if (closeButtonBottom) {

    closeButtonBottom.addEventListener('click', hideModal)
}

let userMenuDropDown = getElement('#btn-user-menu-dropdown')
const toggleUserDropDown = () => {
    const userMenu = getElement('.user-menu-dropdown')
    userMenu.classList.toggle('show-user-menu-dropdown')
}
if (userMenuDropDown) {
    userMenuDropDown.addEventListener('click', toggleUserDropDown)
}
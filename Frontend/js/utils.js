function removeClass(element, cls) {
    element.classList.remove(cls)
}

function addClass(element, cls) {
    element.classList.add(cls)
}

// Crossfade two elements using CSS clases and timers
function crossfade(node1, node2) {
    addClass(node1, 'fade'); // Add fade animation

    addClass(node2, 'fade'); // Add fade animation
    addClass(node2, 'reverse-animation'); // Add animation reverser
    removeClass(node2, 'hidden'); // 'remove hidden class, makes element visible'
    setTimeout(function (node1, node2) {
        node1.setAttribute('display', 'none'); // hide element
        removeClass(node1, 'fade'); // Remove fade animation
        addClass(node1, 'hidden');

        removeClass(node2, 'reverse-animation'); // Remove animation reverser
        removeClass(node2, 'fade'); // Remove fade animation
    }, 400, node1, node2);
}


// this function does nothing, its used when you have
// to provide a fntion or callback but don't need one
function sinkhole() {

}

// Generate a UUID to authenticate as the only valid page instance
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

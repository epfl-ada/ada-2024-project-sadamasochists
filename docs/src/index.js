/* Handle the loading of the page */
window.onload = () => {
    /* Handle the loading screen */
    document.getElementById("loading").style.display = "none";

    /* Hide all the iframes except the first one */
    const iframesContainers = document.getElementsByClassName("iframes_group");
    for (let i=0; i<iframesContainers.length; i++) {
        const iframes = iframesContainers[i].getElementsByTagName("iframe");
        for (let j = 1; j < iframes.length; j++) {
            iframes[j].classList.add("hidden_element");
        }
    }
}
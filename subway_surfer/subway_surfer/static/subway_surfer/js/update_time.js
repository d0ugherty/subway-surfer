/**
 *  Updates the time display in 1 second intervals
 * 
 */

setInterval(() => {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('current-time').textContent = "Current Time: " + timeString;
}, 1000);

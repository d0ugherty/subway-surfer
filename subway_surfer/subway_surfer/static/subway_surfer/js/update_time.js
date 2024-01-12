/**
 *  Updates the time display in 1 second intervals
 * 
 */

function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('current-time').textContent = "Current Time: " + timeString;
}
setInterval(updateTime, 1000); 
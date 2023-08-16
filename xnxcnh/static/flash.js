// xnx-cnh (c) by Vladislav 'ElCapitan' Nazarov
// 
// xnx-cnh is licensed under a
// Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
// 
// You should have received a copy of the license along with this
// work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.
var intervalTimers = new Map();
var animationPaused = false;

document.addEventListener("DOMContentLoaded", function () {
    var flashElements = document.querySelectorAll(".flash");

    flashElements.forEach(function (element) {
        startTimer(element);
    });
});

function startTimer(element) {
    var line = element.querySelector(".line");
    var startTimestamp;
    var remainingTime = 3000;

    function animate(timestamp) {
        if (!startTimestamp) startTimestamp = timestamp;

        var elapsedTime = timestamp - startTimestamp;

        if (elapsedTime >= 10) {
            startTimestamp = timestamp;
            remainingTime -= 10;
            var remainingPercentage = remainingTime / 3000;

            line.style.transform = `scaleX(${remainingPercentage})`;

            if (remainingTime <= 0) {
                element.style.display = "none";
                return;
            }
        }

        if (!animationPaused) {
            requestAnimationFrame(animate);
        }
    }

    animate();
    intervalTimers.set(element, animate);
}

function pauseTimer() {
    animationPaused = true;
}

function resumeTimer() {
    animationPaused = false; 

    var elements = document.querySelectorAll(".flash");

    elements.forEach(function (element) {
        var animateFunc = intervalTimers.get(element);
        if (animateFunc) {
            animateFunc();
        }
    });
}

function disable(element) {
    element.style.display = "none";
}

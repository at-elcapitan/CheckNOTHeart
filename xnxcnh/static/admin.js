// xnx-cnh (c) by Vladislav 'ElCapitan' Nazarov
// 
// xnx-cnh is licensed under a
// Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
// 
// You should have received a copy of the license along with this
// work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

const userctl = document.getElementById("userctl");
const recordctl = document.getElementById("recordctl");

const userctlbtn = document.getElementById("userctlbtn");
const recordctlbtn = document.getElementById("recordctlbtn");

const param = window.location.href.split("#")[1];

if (param == undefined) {
    window.location.href += "#userctl" 
}

if (param == "userctl") {
    userctlbtn.classList.add("inactive");
    recordctlbtn.classList.remove("inactive");

    userctl.style.display = "flex";
    recordctl.style.display = "none";
}

if (param == "recordctl") {
    userctlbtn.classList.remove("inactive");
    recordctlbtn.classList.add("inactive");

    recordctl.style.display = "flex";
    userctl.style.display = "none";
}

userctlbtn.onclick = function () {
    userctlbtn.classList.add("inactive");
    recordctlbtn.classList.remove("inactive");

    userctl.style.display = "flex";
    recordctl.style.display = "none";
}

recordctlbtn.onclick = function () {
    userctlbtn.classList.remove("inactive");
    recordctlbtn.classList.add("inactive");

    recordctl.style.display = "flex";
    userctl.style.display = "none";
}

// at-prs (c) by Vladislav 'ElCapitan' Nazarov
// 
// at-prs is licensed under a
// Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
// 
// You should have received a copy of the license along with this
// work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

const userctl = document.getElementById("userctl");
const recordctl = document.getElementById("recordctl");

const userctlbtn = document.getElementById("userctlbtn");
const recordctlbtn = document.getElementById("recordctlbtn");

userctlbtn.onclick = function() {
    userctlbtn.classList.add("inactive");
    recordctlbtn.classList.remove("inactive");

    userctl.style.display = "block";
    recordctl.style.display = "none";
}

recordctlbtn.onclick = function() {
    userctlbtn.classList.remove("inactive");
    recordctlbtn.classList.add("inactive");

    recordctl.style.display = "block";
    userctl.style.display = "none";
}
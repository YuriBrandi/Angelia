/*const $ = selector => document.querySelector(selector);
$("#find").addEventListener("click", () => {
    console.log("ok");
});*/

document.getElementById("find").addEventListener("click", myFunction);

function myFunction(){
    document.getElementById("find").innerHTML = "YOU CLICKED ME!";
}
getTitle();
document.getElementById("do_btn").addEventListener("click", () => getActiveTab('check_news'));

document.getElementsByClassName("edit")[0].addEventListener("click", function (){
    let text_area = document.getElementById("title_txt");
    text_area.style.display = "inline";
    text_area.style.height = "auto";

    text_area.style.height = text_area.scrollHeight + "px";

    document.getElementById("label_title").style.display = "none";

    document.getElementsByClassName("edit")[0].style.display = "none";
    document.getElementsByClassName("edit")[1].style.display = "inline";
    document.getElementsByClassName("edit")[2].style.display = "inline";
});

document.getElementsByClassName("edit")[1].addEventListener("click", function (){
    document.getElementById("label_title").innerHTML = document.getElementById("title_txt").value;

    document.getElementById("title_txt").style.display = "none";
    document.getElementById("label_title").style.display = "inline";

    document.getElementsByClassName("edit")[0].style.display = "inline";
    document.getElementsByClassName("edit")[1].style.display = "none";
    document.getElementsByClassName("edit")[2].style.display = "none";
});

document.getElementsByClassName("edit")[2].addEventListener("click", function (){
    document.getElementById("title_txt").value = document.getElementById("label_title").innerHTML;

    document.getElementById("title_txt").style.display = "none";
    document.getElementById("label_title").style.display = "inline";

    document.getElementsByClassName("edit")[0].style.display = "inline";
    document.getElementsByClassName("edit")[1].style.display = "none";
    document.getElementsByClassName("edit")[2].style.display = "none";
});
function getTitle() {
   getActiveTab("get_title");
}

function getActiveTab(action) {

    switch (action){
        case "get_title": {
            browser.tabs.query({active: true, currentWindow: true})
                .then(changeTitleText)
                .catch(reportError);
        }break;

        case "check_news": {
            browser.tabs.query({active: true, currentWindow: true})
                .then(checkNews)
                .catch(reportError);
        }break;

        default:
            console.error("getActiveTab 'action' misbehaviour");
    }

}

function extractDomain(url) {
    try {
        const parsedURL = new URL(url);
        return parsedURL.hostname.split('.');
    } catch (error) {
        console.error('Error parsing URL:', error.message);
        return null; // Return null or handle the error as needed
    }
}

function cleanupTitle(title, url) {
    nocomma_title = title.replace(/"/g, "");

    let domain = extractDomain(url);
    console.log("received " + domain);

    // Split the input string into words
    const title_words = nocomma_title.toLowerCase().split(/\s+/);

    // Filter out words that are not in the domain array
    const filteredWords = title_words.filter(word => !domain.includes(word));


    return filteredWords.join(' ');

}

function changeTitleText(tabs) {
    let clean_title = cleanupTitle(tabs[0].title, tabs[0].url)
    document.getElementById("title_txt").value = clean_title;
    document.getElementById("label_title").innerHTML = clean_title;
}

function checkNews(tabs){


    document.getElementById('preContainerImg').innerHTML = "";
    document.getElementById("do_btn").style.display = "none";
    document.getElementById("loading_circle").style.display = "inline";
    document.getElementById("urls").innerHTML = "";
    document.getElementById("output").innerHTML = "";


    document.getElementById("do_img").style.display = "none";
    document.getElementById("btn_text").style.display = "none";

    browser.tabs.sendMessage(tabs[0].id, {
        command: "check_news",
        news_title: document.getElementById("label_title").innerHTML,
        news_url: tabs[0].url
    });
    console.log("Message sent");


}

/**
 * Just log the error to the console.
 */
function reportError(error) {
    console.error(`Could not execute extension: ${error}`);
}


/**
 * There was an error executing the script.
 * Display the popup's error message, and hide the normal UI.
 */
function reportExecuteScriptError(error) {
    //document.querySelector("#popup-content").classList.add("hidden");
    //document.querySelector("#error-content").classList.remove("hidden");
    console.error(`Failed to execute Angelia's content script: ${error.message}`);
}

function reportExectureScriptSuccessful() {
    console.log("Handler Started Successfully");
}

browser.tabs.executeScript({file: "/js/message_handler.js"})
    .then(reportExectureScriptSuccessful)
    .catch(reportExecuteScriptError);

browser.runtime.onMessage.addListener((message) => {
   if(message.command === "getNegScore") {
       document.getElementById("do_btn").style.display = "inline";
       document.getElementById("do_img").style.display = "inline";
       document.getElementById("btn_text").style.display = "inline";
       document.getElementById("loading_circle").style.display = "none";

       console.log("Negativity score: " + message.neg_score + "/100");
       let output_txt = document.getElementById("output")
       output_txt.style.color = "initial";

       if(message.neg_score === -2){
           output_txt.innerHTML = "Due to title extraction limits, we cannot analyze this news.";
       }
       else if(message.neg_score === -1){
           output_txt.style.color = "red";
           output_txt.innerHTML = "No results found 😔";
       }
       else if(message.neg_score === 0){
           output_txt.style.color = "green";
           output_txt.innerHTML = "Trustable ";
       }
       else if(message.neg_score <= 25){
           output_txt.style.color = "yellow";
           output_txt.innerHTML = "Likely Trustable ";
       }
       else if(message.neg_score <= 50){
           output_txt.style.color = "orange";
           output_txt.innerHTML = "Likely Fake ";
       }
       else if(message.neg_score <= 75){
           output_txt.style.color = "red";
           output_txt.innerHTML = "Most Likely Fake ";
       }
       else { //<= 100
           output_txt.style.color = "red";
           output_txt.innerHTML = "Fake! ";
       }

       if(message.neg_score >= 0)
            output_txt.innerHTML += "(" + message.neg_score + "/100)";
   }
   else if(message.command === "getFilteredURLs"){
       for(let element of message.filteredURLs){
           let anchor = document.createElement("a");
           anchor.href = element;
           anchor.innerHTML = element;

           document.getElementById("urls").appendChild(anchor);
           document.getElementById("urls").appendChild(document.createElement("br"));

           if(element !== message.filteredURLs[message.filteredURLs.length - 1])
               document.getElementById("urls").appendChild(document.createElement("br"));
       }
   }
   else if(message.command === "brave_nil"){
       document.getElementById("do_btn").style.display = "inline";
       document.getElementById("do_img").style.display = "inline";
       document.getElementById("btn_text").style.display = "inline";
       document.getElementById("loading_circle").style.display = "none";

       document.getElementById("output").innerHTML = "Check for BRAVE API key and Internet connection.";
       document.getElementById("output").style.color = "red";
   }
});

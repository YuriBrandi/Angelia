getTitle();
document.getElementById("do_btn").addEventListener("click", () => getActiveTab('check_news'));

document.getElementsByClassName("edit")[0].addEventListener("click", function (){
    document.getElementById("title_txt").style.display = "inline";
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
    let domain = extractDomain(url);
    console.log("received " + domain);

    // Split the input string into words
    const title_words = title.toLowerCase().split(/\s+/);

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

    console.log("Message sent");
    browser.tabs.sendMessage(tabs[0].id, {
        command: "check_news",
        news_title: document.getElementById("label_title").innerHTML,
        news_url: tabs[0].url
    });

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
       if(message.neg_score === -1){
           document.getElementById("output").style.color = "red";
           document.getElementById("output").innerHTML = "No results 😔";
       }

       document.getElementById("output").innerHTML = "Negativity Score: " + message.neg_score + "/100";
   }
});

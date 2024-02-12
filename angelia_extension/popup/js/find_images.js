document.getElementById('do_img').addEventListener('click', function() {

    document.getElementById("urls").innerHTML = ""
    document.getElementById('output').innerHTML = ""
    document.getElementById('output').style.color = "white";

    document.getElementById('do_img').style.display = 'none'
    document.getElementById('do_btn').style.display = 'none'
    document.getElementById('btn_text').style.display = 'none'
    document.getElementById('loading_circle').style.display = 'inline'

    const container = document.getElementById('preContainerImg');
    container.innerHTML = ""

    browser.tabs.query({active: true, currentWindow: true})
        .then(tabs => {

            console.log('Message sent')

            browser.tabs.sendMessage(tabs[0].id, {
                command: "image_detection",
                value: true });

        }).catch(error => console.log(error));
});

browser.tabs.executeScript({file: "/js/images_handler.js"})
    .then(()=> console.log('Script images_handler executed'))
    .catch(error => {
        console.error('Error during script execution: ', error);
    });

browser.runtime.onMessage.addListener((message) => {
    if(message.command === "imagesDetection") {
        console.log(message.detections)
        addImagesToPopup(message.detections)
    }
    else if (message.command === "rateLimitReached"){
        console.log(message.detections)
        rateLimitReached()
    }
});

function rateLimitReached(){
    document.getElementById('loading_circle').style.display = 'none'
    document.getElementById('output').style.display = 'inline'
    document.getElementById('do_btn').style.display = 'inline'
    document.getElementById('do_img').style.display = 'inline'
    document.getElementById('btn_text').style.display = 'inline'

    const container = document.getElementById('preContainerImg');
    container.innerHTML = ""

    document.getElementById('output').innerText = 'Rate Limit Reached, Subscribe API Key to Hugging Face or ' +
        'attend 1 hour for reset.'
}

function addImagesToPopup(message){

    document.getElementById('loading_circle').style.display = 'none'
    document.getElementById('do_img').style.display = 'inline'
    document.getElementById('do_btn').style.display = 'inline'
    document.getElementById('btn_text').style.display = 'inline'

    const container = document.getElementById('preContainerImg');
    container.innerHTML = ""

    let images = JSON.parse(message)

    let imageUrls = []

    for (let i = 0; i < images.length; i++){
        if (images[i][1] === 'artificial')
            imageUrls.push(images[i][0])
    }

    document.getElementById('output').style.display = 'inline'
    document.getElementById('output').innerText = 'AI Generated Images Detected: ' + imageUrls.length

    let div;

    for (let i = 0; i < imageUrls.length; i++) {
        const img = document.createElement('img');
        if (i % 3 === 0){
            div = document.createElement('div')
        }
        img.src = imageUrls[i];
        div.appendChild(img);
        container.appendChild(div)
    }
}
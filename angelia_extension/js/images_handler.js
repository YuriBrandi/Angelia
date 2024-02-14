(function () {

    console.log("running images_handler");

    function getAllImagesFromHTML(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        return Array.from(doc.querySelectorAll('img'))
    }

    // extract each image to HTML page and next execute the query
    async function handleQueryToHuggingFace() {

        let json = [];

        const htmlContent = document.documentElement.outerHTML;

        const imageElements = getAllImagesFromHTML(htmlContent);

        let set = new Set();

        for (let i = 0; i < imageElements.length; i++) {
            let imageUrl = imageElements[i].src;

            // image not visible in the page or src not presents or url already used
            if (imageUrl.startsWith('data:') || imageUrl.length === 0 || set.has(imageUrl))
                continue;

            set.add(imageUrl)

            try {
                // request properties of images using a proxy for bypass cors policy
                const response = await fetch('https://corsproxy.io/?' + encodeURIComponent(imageUrl));
                // console.log(response)
                const blob = await response.blob();     // obtains blob file
                // console.log(blob)
                let result = await executeQueryToHuggingFace(blob, imageUrl, imageElements[i]);
                // console.log(imageUrl + ' ' + result);
                result = JSON.parse(result)

                if (Array.isArray(result)){
                    json.push([imageUrl, result[0]['label']])
                }
                else if (result['error'] === 'Rate limit reached. You reached free usage limit (reset hourly). ' +
                    'Please subscribe to a plan at https://huggingface.co/pricing to use the API at this rate'
                    && i === 0)
                    return 'Rate limit reached'

            } catch (error) {
                console.error('Error during download image: ' + imageUrl + '\n', error);
            }
        }

        return json;

    }

    // executes controls for format image and next execute the query to Hugging Face Model
    async function executeQueryToHuggingFace(blob, imageUrl, imgTag){

        let new_url = await checkFormatImage(blob, imageUrl, imgTag);

        if (new_url != null && new_url !== 'error' && new_url !== 'not-valid') {
            const response = await fetch(new_url);
            blob = await response.blob();
        } else if (new_url === 'error') {
            throw new Error('Error during conversions of: ' + imageUrl);
        } else if (new_url === 'not-valid') {
            throw new Error('Image not valid for conversion: ' + imageUrl)
        }

        let response;

        try {
            do {
                response = await fetch(
                    "https://api-inference.huggingface.co/models/Organika/sdxl-detector",
                    {
                        headers: { Authorization: "Bearer " },//<-- API KEYS HERE
                        method: "POST",
                        body: blob,
                    }
                );

                // 503 is service unavailable to Hugging Face
                if (response.status === 503) {
                    await new Promise(resolve => setTimeout(resolve, 2000)); // Attends 2 seconds
                }

            } while (response.status === 503); // repeats the query
        } catch (error) {
            console.error('Error during the request API: ', error);
        }

        const result = await response.json();
        return JSON.stringify(result);
    }

    /*
     *  uses standard API of browser, therefore there might be security problem. Create canvas and draw imageBitmap inside,
     *  finally return the new url of image
     */
    async function convertImageOtherFormats(blob) {
        let canvas = document.createElement("canvas");
        let context = canvas.getContext("2d");
        const imageBitmap = await createImageBitmap(blob);

        canvas.width = imageBitmap.width;
        canvas.height = imageBitmap.height;
        context.drawImage(imageBitmap, 0, 0);

        return canvas.toDataURL("image/png");
    }

    // convert .svg image to image/png using the canvas
    function convertSVG(imgTag) {
        let canvas = document.createElement("canvas");
        let ctx = canvas.getContext("2d");

        canvas.width = imgTag.width;
        canvas.height = imgTag.height;
        ctx.drawImage(imgTag, 0, 0);

        return canvas.toDataURL("image/png");
    }

    async function checkFormatImage(blob, imageUrl, imgTag) {

        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif', 'image/tiff', 'image/bmp',
            'image/vnd.microsoft.icon']

        // console.log(blob.type)

        if (!allowedTypes.includes(blob.type)) {
            try {
                if (blob.type === 'text/html; charset=utf-8' || blob.type === 'application/json'
                    || blob.type === 'text/html;charset=utf-8' || blob.type === 'text/plain'
                    || blob.type === 'text/html; charset=iso-8859-1' || (imgTag.width === 1 && imgTag.height === 1))
                    return Promise.resolve('not-valid');
                else if (blob.type === 'image/svg+xml')
                    return convertSVG(imgTag);
                else
                    return await convertImageOtherFormats(blob);
            } catch (error) {
                return Promise.resolve('error');
            }
        }

        // return null if the type is consented
        return Promise.resolve(null);
    }

    browser.runtime.onMessage.addListener(async (message) => {

        if (message.command === "image_detection") {

            console.log('Message received')

            let result = await handleQueryToHuggingFace();

            console.log(result)

            if (Array.isArray(result)){
                browser.runtime.sendMessage({
                    command: "imagesDetection",
                    detections: JSON.stringify(result)
                });
            }
            else {
                browser.runtime.sendMessage({
                    command: "rateLimitReached",
                    detections: null
                });
            }
        }
    });


})();
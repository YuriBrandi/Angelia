# Angelia (/aŋ.ɟeˈli.a/):

### An open-source lightweight Fake news detector based on NLP Machine Learning models.

<p align='center'> 
    <img src=https://github.com/YuriBrandi/Angelia/assets/52039988/fe187280-24c1-4878-b211-98daf4e485d4 width=200>
</p>

This University work consists of an in-depth study and a fully working *privacy-oriented*, *open-source*, *lightweight* browser extension that allows to **verify** *Fake news' titles* and *AI synthetic images*. 

It is inspired by the earlier paper [ConvNet frameworks for multi-modal fake news detection](https://link.springer.com/article/10.1007/s10489-021-02345-y), which uses trusted sources and polarity analysis for fake news detection.

### Authors
[@raffaele-aurucci](https://github.com/raffaele-aurucci), [@LukaszG92](https://github.com/LukaszG92), [@YuriBrandi](https://github.com/YuriBrandi).

## Contributions

Contributions are very much appreciated. Please well describe your changes inside your PR to make it easier to understand them.

If you encounter any problem or bug that is unrelated with your own machine, please report it and *open a new issue* with replicable steps. 

## Workflow

<p align='center'> 
    <img width="589" src="https://github.com/YuriBrandi/Angelia/assets/52039988/1c90020c-4805-46e9-b784-0c4f5b48e4e7">
</p>

This work will be followed by a scientific paper, thus technical information won't be covered in this readme.

*Angelia* consist of 4 main modules:

- A Sentiment Analysis module
- A Tokenization module
- A Title Extraction module
- A Reliability Evaluation module

#### Note: All these modules are exectued in local and require no external requests (no CDN is used).

![Angelia-EnglishW](https://github.com/YuriBrandi/Angelia/assets/52039988/d11fe413-e9fe-46cd-95db-cb13eaf21fb1)

1. The extension extracts the title, and tokenizes it to facilitate News search via the API.
2. Each result is filtered by hostname through a list of **TNS** (Trusted News Sites).
3. The sentiment of the original title is compared to the one of the filtered news, this allows the polarity of news' titles to be compared.

The reliability evaluation module is in continuous development. At the moment, the polarity of each news is compared and a negativity score is given, which results in a textual outcome (e.g. *Likely Fake*, *Trustable* ...). When faced with negative-polarity comparisons, the extensions utilizes heuristics found in our studies, for instance it checks for words of disagreement such as *"No, ..."* Or *"Fake ..."*.

The sentiment analysis module is powered by the [Pyodide](https://github.com/pyodide/pyodide) interpreter, customized and lightened to the bare minimum to offer a fast and serverless experience. All the libraries come already included in the extension and no external resource is fetched.

Finally, Angelia comes with an experimental functionality to detect **AI synthetic images** inside web pages. In this case the extension has 3 main modules:

- Image's Format Evaluation module
- Converter Image's Format module
- AI Image Detector module

![AngeliaImages-English](https://github.com/YuriBrandi/Angelia/assets/114738583/809608dd-7963-4de4-82f2-cd3950d78e34)

1. The extension extracts all images from HTML page and relative URLs.
2. Executes a request for each image's url using a free [Proxy](https://corsproxy.io/).
3. Each image's format is checked by MIME type and sent via BLOB format to the [SDXL Detector Model](https://huggingface.co/Organika/sdxl-detector) hosted in Hugging Face, using the API.
4. If the image's format is invalid for classification, the extension draws the images into HTML page using a canvas, and converts all in *image/png*. Next it obtains new BLOB by this new images and relative URLs, ready for sent to the model hosted in Hugging Face.

#### Note: False positives might sometimes occur, therefore please manually double-check an image before judging its authenticity.

## Installing the extension 

Since it is still in an early stage development, at the moment *Angelia* is still not available in the Extensions store. But we plan to migrate to Manifest v3 and to port the work to *Chromium* browsers soon.

Simply **Download the .zip** in the *Releases* section, alternatively you can **clone this repo**.

**Then:**

- The extensions uses the [Brave Search API](https://brave.com/search/api/) to look for news,
please remember to insert a subscription token in ```Angelia/angelia_extension/js/message_handler.js``` *(line 18)* to make the API calls work.
Getting an API token is fairly simple and also free https://brave.com/search/api/.

- Angelia also uses the [Hugging Face API](https://huggingface.co/docs/api-inference/quicktour) to detect AI images inside news,
please remember to insert a subscription token in ```Angelia/angelia_extension/js/images_handler.js``` *(line 79)* to make the API calls work *(you can skip this step if not interested in this feature)*
As for Brave, an Hugging Face API token is also free to get https://huggingface.co/docs/api-inference.

Please feel free to try implementing different APIs and let us know :).

Finally go to ```about:debugging``` in your Firefox (or Firefox-based) browser and add the extension from ```Angelia/angelia_extension/manifest.json```.

## References
This repository borrows partially from [CNNDetection](https://github.com/PeterWang512/CNNDetection) and [GANImageDetection](https://github.com/grip-unina/GANimageDetection) repositories.

## License

This project is distributed under the [GNU General Public License v3](LICENSE).

![GPLv3Logo](https://www.gnu.org/graphics/gplv3-127x51.png)

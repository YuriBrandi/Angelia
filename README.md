# Angelia: 

### A Fake news detector based on NLP Machine Learning models.

<p align='center'> 
    <img src=https://github.com/YuriBrandi/Angelia/assets/52039988/fe187280-24c1-4878-b211-98daf4e485d4 width=200>
</p>

### Authors
[@raffaele-aurucci](https://github.com/raffaele-aurucci), [@LukaszG92](https://github.com/LukaszG92), [@YuriBrandi](https://github.com/YuriBrandi).

This University work consists of an in-depth study and a fully working Firefox Extension inspired by the earlier paper [ConvNet frameworks for multi-modal fake news detection](https://link.springer.com/article/10.1007/s10489-021-02345-y), which uses trusted sources and polarity analysis for fake news detection.

## Contributions

Contributions are very much appreciated. Please well describe your changes inside your PR to make it easier to understand them.

If you encounter any problem or bug that is unrelated with your own machine, please report it and *open a new issue* with replicable steps. 

## Workflow

<p align='center'> 
    <img width="589" src="https://github.com/YuriBrandi/Angelia/assets/52039988/d2ceddf1-c1dd-48be-8d79-4f3a8e19a937">
</p>

This work will be followed by a scientific paper, thus technical information won't be covered in this readme.

*Angelia* consist of 4 main modules:

- A Sentiment Analysis module
- A Tokenization module
- A Title Extraction module
- A Reliability Evaluation module

#### Note: All these modules are exectued in local and require no external requests.

![Angelia-EnglishW](https://github.com/YuriBrandi/Angelia/assets/52039988/d11fe413-e9fe-46cd-95db-cb13eaf21fb1)

1. The extension extracts the title, and tokenizes it to facilitate News search via the API.
2. Each result is filtered by hostname through a list of **TNS** (Trusted News Sites).
3. The sentiment of the original title is compared to the one of the filtered news, this allows the polarity of news' titles to be compared.

The reliability evaluation model is in continuous development. At the moment, the polarity of each news is compared and a negativity score is given. When faced with negative-polarity comparisons, the extensions checks for words of disagreement such as "No, ...." Or "Fake ...".

## Installing the extension 

Since it is still in an early stage development, at the moment *Angelia* is still not available in the Extensions store. But we plan to migrate to Manifest v3 and to port the work to *Chromium* browsers soon.

Simply **clone this repo** (you can use GitHub's interface as well).
 ```bash 
git clone https://github.com/YuriBrandi/Angelia.git
```

The extensions uses the [Brave Search API](https://brave.com/search/api/) to look for news,
please remember to insert a subscription token in ```Angelia/angelia_extension/js/message_handler.js``` *(line 18)* to make the API calls work.
Getting an API token is fairly simple and also free https://brave.com/search/api/.

Please feel free to try different APIs and let us know :).

Finally go to ```about:debugging``` in your Firefox (or Firefox-based) browser and add the extension from ```Angelia/angelia_extension/manifest.json```.

## References
This repository borrows partially from [CNNDetection](https://github.com/PeterWang512/CNNDetection) and [GANImageDetection](https://github.com/grip-unina/GANimageDetection) repositories.

## License

This project is distributed under the [GNU General Public License v3](LICENSE).

![GPLv3Logo](https://www.gnu.org/graphics/gplv3-127x51.png)

# Angelia: 

### A Fake news detector based on NLP Machine Learning models.

<p align='center'> 
    <img src=https://github.com/musimathicslab/JAMintheMLoop/assets/52039988/7bf38b1c-293b-4662-a5aa-34a35c9f7703 width=200>
</p>

### Authors
@raffaele-aurucci, @LukaszG92, @YuriBrandi.

This University work consists of an in-depth study and a fully working Firefox Extension inspired by the earlier paper [ConvNet frameworks for multi-modal fake news detection](https://link.springer.com/article/10.1007/s10489-021-02345-y), which uses trusted sources and polarity analysis for fake news detection.

## Contributions

Contributions are very much appreciated. Please well describe your changes inside your PR to make it easier to understand them.

If you encounter any problem or bug that is unrelated with your own machine, please report it and *open a new issue* with replicable steps. 

## How does it work

## How to install the extension

Since it is still in an early stage development, at the moment *Angelia* is still not available in the Extensions store. But we plan to migrate to Manifest v3 and to port the work to *Chromium* browsers soon.

Simply **clone this repo** (you can use GitHub's interface as well).
 ```bash 
git clone https://github.com/YuriBrandi/Angelia.git
```

The extensions uses the [Brave Search API](https://brave.com/search/api/) to look for news,
please remember to insert a subscription token in ```Angelia/angelia_extension/js/message_handler.js``` *(line 18)* to make the API calls work.
Getting an API token is fairly simple and also free https://brave.com/search/api/.

Please feel free to try different APIs and let us know :).

Finally go to [about:debugging](about:debugging) in your Firefox (or Firefox-based) browser and add the extension from ```Angelia/angelia_extension/manifest.json```.

## References

## License

This project is distributed under the [GNU General Public License v3](LICENSE).

![GPLv3Logo](https://www.gnu.org/graphics/gplv3-127x51.png)

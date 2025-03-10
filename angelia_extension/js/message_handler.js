(function() {
    console.log("Angelia's content script loaded successfully");



    const BRAVE_URL = "https://api.search.brave.com/res/v1/web/search?q="


    const OPTIONS = {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': '' //<-- YOUR KEY GOES HERE!
        }
    }

    const TRUSTED_SITES = [
        'www.nytimes.com',
        'www.wsj.com',
        'www.washingtonpost.com',
        'www.bbc.com',
        'www.economist.com',
        'www.newyorker.com',
        'www.ap.org',
        'www.reuters.com',
        'www.bloomberg.com',
        'www.foreignaffairs.com',
        'www.theatlantic.com',
        'www.politico.com',
        'www.c-span.org',
        'www.thebureauinvestigates.com',
        'www.csmonitor.com',
        'www.npr.org',
        'www.propublica.org',
        'eu.usatoday.com',
        'fair.org',
        'www.pewresearch.org',
        'www.pbs.org',
        'www.cbsnews.com',
        'www.theguardian.com',
        'edition.cnn.com',
        'www.nbcnews.com',
        'www.forbes.com',
        'theconversation.com',
        'www.upi.com',
        'journalistsresource.org',
        'www.snopes.com',
        'www.huffpost.com',
        'www.foxnews.com',
        'www.dailymail.co.uk',
        'www.avclub.com',
        'www.bandcamp.com',
        'www.vulture.com',
        'www.pitchfork.com',
        'www.rollingstone.com',
        'www.upworthy.com',
        'www.variety.com',
        'www.vibe.com',
        'www.deadline.com',
        'www.heavy.com',
        'www.indiewire.com',
        'www.imdb.com'
    ];

    //const natural = require('natural');
    //const tokenizer = new natural.WordTokenizer();
    /**
     * Check and set a global guard variable.
     * If this content script is injected into the same page again,
     * it will do nothing next time.
     */
    if (window.hasRun) {
        return;
    }
    window.hasRun = true;


    async function loadWASMInterpreter(){

        let pyodide = await loadPyodide();
        const fileURL = browser.runtime.getURL('js/pyodide/textblob-0.17.1-py2.py3-none-any.whl');

        // Fetch the contents of the file
        return fetch(fileURL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch file');
                }
                return response.url // Return the response body as text
            })
            .then(async file => {
                await pyodide.loadPackage([file]);
                await pyodide.loadPackage("nltk");

                console.log("Python Interpreter and Libraries have all been loaded correctly ✓");
                return pyodide;
            })
            .catch(error => {
                console.error('Error fetching file:', error);
                return error;
            });

    }

    function isTitleAffirmative(sentence) {
        sentence = sentence.toLowerCase();
        return !(sentence.includes('fake') || sentence.includes('false')
            || sentence.startsWith('no ') || sentence.startsWith('no,') || sentence.startsWith('no.'));

    }

    function filterArrayByTrusted(array){
        let filteredHostnames = [];
        for(let element of array){
            if(TRUSTED_SITES.includes(element[0]))
                filteredHostnames.push(element); //Push all array
        }

        console.log("Trusted entries # (filtered): " + filteredHostnames.length);
        return filteredHostnames;
    }

    function getSimplifiedArray(jsonResults) {
        let hostnames = [];
        for(let i = 0; i < jsonResults.web.results.length; i++)
            hostnames.push([jsonResults.web.results[i].meta_url.hostname, jsonResults.web.results[i].title,
                jsonResults.web.results[i].url]);
            //console.log(jsonResults.web.results[i].meta_url.hostname); Debug

        console.log("# Total entries: " + hostnames.length);
        return hostnames;
    }

    function sendNewsURLs(filteredArray) {

        let urls_array = [];

        for(element of filteredArray) //Element[2] contains news url.
            urls_array.push(element[2]);


        browser.runtime.sendMessage({
            command: "getFilteredURLs",
            filteredURLs: urls_array
        });

    }

    function evaluateTrust(filteredArray, titleSentiment, titleAffirmation, interpreter) {
        /*
            Final negativity score = number of contradicting news/number of evaluated news.
         */
        let contradictory_score = 0;

        let neutrality_score = 0;

        if(filteredArray.length == 0)
            return -1; //Special score for no filtered result returned.

        for(let element of filteredArray){
            console.log(element);
            //Element[1] contains news' title, Element[0] contains news' hostname.
            let sentiment = getSentiment(interpreter, cleanupTitleFromHostname(element[1], element[0]));

            if(sentiment === 0){
                neutrality_score++;
                continue;
            }

            //If sentiments score are of opposed value, then increase the contradictory score.
            if(sentiment * titleSentiment < 0)
                contradictory_score++;


            /*
                From our study, titles can be both negative but still contradicting
                if they have opposite affirmation.

                E.g.: Young teen dies tragically in car accident: -0.5.
                E.g.: Fake News: Young teen did not die in car accident: -0.6.

                This behaviour can be predicted by checking words such as
                'Fake' or 'No, ...' at the beginning of a title
             */
            else if(titleSentiment < 0 && sentiment < 0
                && titleAffirmation !== isTitleAffirmative(element[1]))
                contradictory_score++;

        }

        console.log("Contradictory score: " + contradictory_score);
        console.log("Neutrality score: " + neutrality_score);

        if(neutrality_score === filteredArray.length)
            return -2;

        return Math.round((contradictory_score/(filteredArray.length - neutrality_score))*100);
    }

    async function doSearchQuery(sentence) {
        /*
            Source: Brave API documentation: https://api.search.brave.com/app/documentation/web-search/get-started

            curl -s --compressed "https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain" -H
            "Accept: application/json" -H "Accept-Encoding: gzip" -H "X-Subscription-Token:
            <YOUR_API_KEY>"*/

        /*
            Add sentence with '+' symbol separation to the url for the Query search
         */

        console.log("Searching " + sentence.replace(/ /g, '+'));
        let json_data = await fetch(BRAVE_URL + sentence.replace(/ /g, '+'), OPTIONS)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // Handle the response data as needed
                return data;

            })
            .catch(error => {
                console.error('Fetch error:', error);
                console.error("CHECK FOR BRAVE API KEY and Internet connection.");
                return null;
            });

        return json_data;

    }

    function getSentiment(interpreter, sentence) {


         return interpreter.runPython(`
                        from textblob import TextBlob
                        blob = TextBlob("${sentence}")
                        sentiment = blob.sentiment
                        print(sentiment)
                        sentiment.polarity
                    `);
    }

    function tokenize(title) {


        let tokenized_title = title.split(/\W+/).filter(function(token) {
           return token.length > 3;

        });

        console.log(tokenized_title);
        return tokenized_title.join(' '); //Transform to space separated sentence
    }

    function cleanupTitleFromHostname(title, hostname) {
        nocomma_title = title.replace(/"/g, "");
        let domain = hostname.split('.');
        console.log("received " + domain);

        // Split the input string into words
        let title_words = nocomma_title.toLowerCase().split(/\s+/);

        // Filter out words that are not in the domain array
        let filteredWords = title_words.filter(word => !domain.includes(word));


        return filteredWords.join(' ');

    }

    /**
     * Listen for messages from the background script.
     * Call "beastify()" or "reset()".
     */
    browser.runtime.onMessage.addListener((message) => {

        if (message.command === "check_news") {
            console.log("message 'check_news' received");


            loadWASMInterpreter()
                .then(interpreter => {

                   let pyodide = interpreter;

                   let original_sentiment =  getSentiment(pyodide, message.news_title);

                   console.log("Original sentiment: " + original_sentiment);

                   if(original_sentiment === 0){
                       browser.runtime.sendMessage({
                           command: "getNegScore",
                           neg_score: -2
                       });
                       return;
                   }

                   let tokenized_title = tokenize(message.news_title);

                    //do Brave Search with Async function
                    doSearchQuery(tokenized_title)
                        .then(data => {
                            if(data == null){
                                browser.runtime.sendMessage({
                                    command: "brave_nil",
                                });
                            }

                            //Reduce the json to an array of [hostname, title]
                            let simple_array = getSimplifiedArray(data);
                            //console.log(hostnames);


                            //Filter the array by Trusted Sites
                            let filtered_array = filterArrayByTrusted(simple_array);

                            //send URLs
                            sendNewsURLs(filtered_array);

                            //returns a negativity score.
                            let neg_score = evaluateTrust(filtered_array, original_sentiment, isTitleAffirmative(message.news_title), pyodide);
                            console.log('negativity score: ' + neg_score);

                            browser.runtime.sendMessage({
                                command: "getNegScore",
                                neg_score: neg_score
                            });
                        });

                    //performSearch(tokenized_title);
                });

        }
    });

})();

(function() {
    console.log("running");


    /*var Sentiment = require(['index.js'], function(foo){

    });*/

    var Sentiment = require('sentiment');

    const url = "https://api.search.brave.com/res/v1/web/search?q="

    const options = {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': '' //<-- YOUR KEY GOES HERE!
        }
    }

    const trustedSites = [
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
        'www.dailymail.co.uk'
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


    function isTitleAffirmative(sentence) {
        sentence = sentence.toLowerCase();
        return !(sentence.includes('fake') || sentence.includes('false')
            || sentence.startsWith('no ') || sentence.startsWith('no,') || sentence.startsWith('no.'));

    }

    function filterArrayByTrusted(array){
        let filteredHostnames = [];
        for(let element of array){
            if(trustedSites.includes(element[0]))
                filteredHostnames.push(element); //Push all array
        }

        console.log("Trusted entries # (filtered): " + filteredHostnames.length);
        return filteredHostnames;
    }

    function getSimplifiedArray(jsonResults) {
        let hostnames = [];
        for(let i = 0; i < jsonResults.web.results.length; i++)
            hostnames.push([jsonResults.web.results[i].meta_url.hostname, jsonResults.web.results[i].title]);
            //console.log(jsonResults.web.results[i].meta_url.hostname); Debug

        console.log("# Total entries: " + hostnames.length);
        return hostnames;
    }

    function evaluateTrust(filteredArray, titleSentiment, titleAffirmation) {
        /*
            Final negativity score = number of contradicting news/number of evaluated news.
         */
        let contradictory_score = 0;
        
        for(let element of filteredArray){
            //console.log(element);
            let sentiment = getSentiment( //Element[1] contains news' title, Element[0] contains news' hostname.
                tokenize(element[1], element[0].split('.'))); //extractDomain call not needed as element[0] is already a hostname.

            //If sentiments are contradicting, then increase score.
            if((sentiment < 0 && titleSentiment > 0)
                || (sentiment > 0 && titleSentiment < 0))
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

        if(filteredArray.length == 0)
            return 0;
        
        return Math.round((contradictory_score/filteredArray.length)*100);
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
        let json_data = await fetch(url+sentence.replace(/ /g, '+'), options)
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
            });

        return json_data

    }
    function getSentiment(sentence) {
        var sentiment = new Sentiment();
        var result = sentiment.analyze(sentence);

        //console.log(result.comparative); // Outputs a sentiment score
        return result.comparative;
    }
    function tokenize(title, domains) {
        console.log("received " + domains);

        let tokenized_title = title.split(/\W+/).filter(function(token) {
           return domains.indexOf(token.toLowerCase()) == -1 && token.length > 3;

        });

        console.log(tokenized_title);
        return tokenized_title.join(' '); //Transform to space separated sentence
    }

    function extractDomains(url) {
        try {
            const parsedURL = new URL(url);
            return parsedURL.hostname.split('.');
        } catch (error) {
            console.error('Error parsing URL:', error.message);
            return null; // Return null or handle the error as needed
        }
    }


    /**
     * Listen for messages from the background script.
     * Call "beastify()" or "reset()".
     */
    browser.runtime.onMessage.addListener((message) => {

        if (message.command === "check_news") {
            console.log("message 'check_news' received");
            let summarized_title = tokenize(message.news_title, extractDomains(message.news_url));

            let original_sentiment =  getSentiment(summarized_title);

            //do Google Search with Async function
            doSearchQuery(summarized_title)
                .then(data => {
                    //Reduce the json to an array of [hostname, title]
                    let simple_array = getSimplifiedArray(data);
                    //console.log(hostnames);
                    //Filter the array by Trusted Sites
                    let filtered_array = filterArrayByTrusted(simple_array);

                    //returns a negativity score.
                    let neg_score = evaluateTrust(filtered_array, original_sentiment, isTitleAffirmative(message.news_title));
                    console.log('negativity score: ' + neg_score);

                    browser.runtime.sendMessage({
                        command: "getNegScore",
                        neg_score: neg_score
                    });


                });

        }
    });

})();

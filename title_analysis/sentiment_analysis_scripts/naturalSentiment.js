const natural = require('natural');
const fs = require('fs');
const csv = require('csv-parser');
const tokenizer = new natural.WordTokenizer();
let analyzer = new natural.SentimentAnalyzer('English', natural.PorterStemmer, 'afinn');

function getLabel(text) {
    let sentiment = analyzer.getSentiment(tokenizer.tokenize(text));
    if(sentiment < 0)
        return "NEGATIVE";
    if(sentiment === 0)
        return "NEUTRAL";
    if(sentiment > 0)
        return "POSITIVE";
}

let sentimentScore = 0;
let heuristicsScore = 0;
let csvLen = 0;

fs.createReadStream('../datasets/titles_dataset.csv')
    .pipe(csv())
    .on('data', (row) => {
        csvLen++;
        if(getLabel(row['real_news']) !== getLabel(row['fake_news']))
           sentimentScore++;
        else {
            if (row['real_news'].toLowerCase().includes('fake'))
                heuristicsScore++;
            else if (row['real_news'].toLowerCase().includes('false'))
                heuristicsScore++;
            else if (row['real_news'].toLowerCase().startsWith('no '))
                heuristicsScore++;
            else if (row['real_news'].toLowerCase().startsWith('no,'))
                heuristicsScore++;
            else if (row['real_news'].toLowerCase().startsWith('no.'))
                heuristicsScore++;
        }
    })
    .on('end', () => {
        console.log(`sentimentScore ${sentimentScore}; in %: ${(sentimentScore / csvLen) * 100}.\ntotalScore ${sentimentScore + heuristicsScore}; in %: ${((sentimentScore + heuristicsScore) / csvLen) * 100}`);
    });
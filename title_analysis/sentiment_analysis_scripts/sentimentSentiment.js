const Sentiment = require('sentiment');
const fs = require('fs');
const csv = require('csv-parser');
let sentiment = new Sentiment();
function getLabel(text) {
    let sentimentResult = sentiment.analyze(text);
    if(sentimentResult.comparative < 0)
        return "NEGATIVE";
    if(sentimentResult.comparative === 0)
        return "NEUTRAL";
    if(sentimentResult.comparative > 0)
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
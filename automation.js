let puppeteer = require('puppeteer');
let minimist = require('minimist');
let { spawn } = require('child_process');

let args = minimist(process.argv);

main();

async function main(){
    let browser = await puppeteer.launch({
        headless: false,
        args: [
            '--start-maximized'
        ],
        defaultViewport: null
    })

    let pages = await browser.pages();
    let page = pages[0];
    let mainurl = "https://www.imdb.com"
    await page.goto(mainurl)

    await page.waitForSelector("input[id='suggestion-search']")
    await page.type("input[id='suggestion-search']", args.name)

    await page.waitForSelector("a[data-testid='search-result--const']")
    let url = await page.$$eval("a[data-testid='search-result--const']", function(turls){
        let urls = []
        for(let i = 0; i < turls.length; i++){
            let surl = turls[i].getAttribute("href");
            urls.push(surl);
        }
        return urls;
    });

    let suburl = url[0];
    let combinedUrl = mainurl + suburl
    await page.goto(combinedUrl)

    let pyScript = spawn('python', ['beautifulsoup.py', combinedUrl])
    pyScript.stdout.on('data', (data) => {
        success(data)
    });
    browser.close();
}
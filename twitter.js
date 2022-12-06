const { email, id, password } = require('./private.js');
const { login } = require('./twitter_login.js');
const { Builder, By, until, Key } = require('selenium-webdriver');
const fs = require('fs');
// console.log(Key)
// return
const nickName = "mizuki_i_l";

// 트위터 크롤링
const start =  async () => {
	let driver = await new Builder('./chromedriver').forBrowser('chrome').build();
	await driver.get('https://twitter.com/i/flow/login');
	await driver.manage().window().maximize();

	// 메인 브라우저 값 저장
	const defaultHandle = await driver.getWindowHandle();
	
	// 트위터 로그인
	login(driver, email, id, password);

	// 트윗 내용 크롤링
	await driver.wait(until.elementLocated(By.css('[data-testid="cellInnerDiv"]')));
	await driver.get(`https://twitter.com/${nickName}`);
	
	// 트윗 링크 리스트
	let tweetsLink = [];
	
	try {
		while(1) {
			let replyCount = 0;
			await driver.wait(until.elementLocated(By.css('[data-testid="cellInnerDiv"]')));
			await driver.findElement(By.css('[data-testid=cellInnerDiv] [data-testid=app-text-transition-container]')).getText().then(function(text) {
				replyCount = Number(text);
			});
			
			// 리플 갯수 1개 이상에서만 실행
			if (0 < replyCount) {
				const tweetLinkTag = await driver.findElements(By.css('[data-testid=cellInnerDiv]:first-child a[role=link]'));
				const urlPatten = new RegExp(`${nickName}/status/.*`);
				const urlPatten2 = new RegExp(`photo`);
				for (let i = 0; i < tweetLinkTag.length; i++) {
					let tweetLink = await tweetLinkTag[i].getAttribute('href');
					if (urlPatten.test(tweetLink) && !urlPatten2.test(tweetLink)) {
						tweetsLink.push(tweetLink);
						console.log(tweetsLink)
					}
				}
			}
		
			//트윗 block 삭제
			await driver.wait(until.elementLocated(By.css('[data-testid="cellInnerDiv"]')));
			await driver.executeScript(`
				document.querySelector('[data-testid="cellInnerDiv"]').remove();
			`);
			await driver.sleep(100);
		}
	} catch (error) {

		tweetsLink.forEach()
		fs.writeFile('links.txt', "tweetsLink", 'utf8', function(error){
			console.log('write end!')
		});
	}

	// await driver.quit();
};

const userAccess =  async (nickName) => {
	await driver.wait(until.elementLocated(By.css('[data-testid="cellInnerDiv"]')));
	await driver.get(`https://twitter.com/${nickName}`);
}

(async ()=>{
	await start();
})();
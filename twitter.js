const { email, id, password } = require('./private.js');
const { Builder, By, until, Key } = require('selenium-webdriver');

//트위터 크롤링
const start =  async () => {
	let driver = await new Builder('./chromedriver').forBrowser('chrome').build();
	await driver.get('https://twitter.com/i/flow/login');
	await driver.manage().window().maximize();

	//메인 브라우저 값 저장
	const defaultHandle = await driver.getWindowHandle();

	console.log(email)
	console.log(id)
	console.log(password)
	
	//이메일 입력
	await driver.wait(until.elementLocated(By.css('[name=text]')));
	// await driver.executeScript(`
	// 	document.querySelector('[name=text]').value = '${email}';
	// `);
	// await driver.sleep(3500);
	await driver.findElement(By.css('[name=text]')).sendKeys(email, Key.ENTER);

	//id 입력
	await driver.wait(until.elementLocated(By.css('[name=text]')));
	// await driver.executeScript(`
	// 	document.querySelector('[name=text]').value = '${id}';
	// `);
	await driver.findElement(By.css('[name=text]')).sendKeys(id, Key.ENTER);

	//password 입력
	await driver.wait(until.elementLocated(By.css('[name=password]')));
	// await driver.executeScript(`
	// 	document.querySelector('[name=text]').value = '${password}';
	// `);
	await driver.findElement(By.css('[name=password]')).sendKeys(password, Key.ENTER);

	// await driver.quit();
};

(async ()=>{
	await start();
})();
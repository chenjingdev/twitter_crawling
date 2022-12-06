const { Builder, By, until, Key } = require('selenium-webdriver');

exports.login = async function(driver, email, id, password) {
	
	//이메일 입력
	await driver.wait(until.elementLocated(By.css('[name=text]')));
	await driver.findElement(By.css('[name=text]')).sendKeys(email, Key.ENTER);

	//id 입력
	await driver.wait(until.elementLocated(By.css('[name=text]')));
	await driver.findElement(By.css('[name=text]')).sendKeys(id, Key.ENTER);

	//password 입력
	await driver.wait(until.elementLocated(By.css('[name=password]')));
	await driver.findElement(By.css('[name=password]')).sendKeys(password, Key.ENTER);
}
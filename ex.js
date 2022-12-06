const { Builder, By, until, Key } = require('selenium-webdriver');

//Information ''내에 정보 입력
const Information = {
    nid : '네이버아이디',
    npw : '네이버비번',
    keyword : '키워드',
    comment : '댓글 내용',
    count : 30
};

let commentCount = Information.count;

//지식인 자동 댓글
const KinAutoComment =  async (nid,npw,keyword,comment) => {
    let driver = await new Builder('./chromedriver').forBrowser('chrome').build();
    await driver.get('https://www.naver.com');
    await driver.wait(until.elementLocated(By.css('#footer')));

    //메인 브라우저 값 저장
    const defaultHandle = await driver.getWindowHandle();
    //console.log('기본 핸들 저장 완료');
    
    //로그인
    await Nlogin(driver,nid,npw);
    
    //검색어 입력
    await NSearch(driver,keyword);

    //지식인 탭 이동
    await MoveToKin(driver);

    //지식인 댓글 모든 페이지 자동
    await KinAutoWritePages(driver,defaultHandle,comment);

    //종료
    console.log('끝');
    await driver.quit();
};

//네이버 로그인
const Nlogin = async (driver,nid,npw)=>{
    //로그인
    const loginBtn = await driver.findElement(By.css(`a.link_login`));
    await loginBtn.click();
    //console.log('로그인 화면 전환 완료');

    //대기 (아이디 비번)
    await driver.wait(until.elementLocated(By.css('#id')));
    await driver.wait(until.elementLocated(By.css('#pw')));

    //아이디 비번 입력
    await driver.executeScript(`
        document.querySelector('#id').value = '${nid}';
        document.querySelector('#pw').value = '${npw}';
    `);

    //대기 (로그인 버튼)
    await driver.wait(until.elementLocated(By.css('.btn_global')));
    //console.log('아이디 비번 입력 완료');

    //로그인 버튼 클릭
    const loginSubmit = await driver.findElement(By.css(`.btn_global`));
    await loginSubmit.click();
    //console.log('로그인 버튼 클릭 완료');
    
    //대기 (등록안함 버튼)
    await driver.wait(until.elementLocated(By.css('.btn_cancel > .btn')));
    
    //등록안함 버튼 클릭
    //아이디 비번 입력
    const afterLoginBtn = await driver.findElement(By.css('.btn_cancel > .btn'));
    await afterLoginBtn.click();
    //console.log('등록안함 버튼 클릭 완료');
}

//네이버 키워드 검색
const NSearch = async (driver,keyword)=>{
    //대기 (검색어 입력)
    await driver.wait(until.elementLocated(By.css('#query')));
    //검색어 입력
    const searchTag = driver.findElement(By.css('#query'));
    await searchTag.sendKeys(keyword, Key.ENTER);
    //console.log(`검색어(${keyword}) 입력 완료`);
}

// 지식인 탭 이동
const MoveToKin = async (driver)=>{
    //대기 (탭검색)
    await driver.wait(until.elementLocated(By.css('#footer')));
    //탭 검색
    const menuTab = await driver.findElement(By.css('ul.base'));
    const menuItems = await menuTab.findElements(By.css('li.menu a'));
    for (let i = 0; i < menuItems.length; i++) {
        let inText = await menuItems[i].getText();
        if (inText === '지식iN'){
            await menuItems[i].click();
            break;
        }
    }
    //console.log('지식인 탭 이동 완료');
}

//다음 페이지 존재 여부 확인
const CanMoveNextPage = async(driver) =>{
    //대기 (글목록 검색)
    await driver.wait(until.elementLocated(By.css('#footer')));
    //페이지 검색
    let btn_next = await driver.findElement(By.css('.sc_page .btn_next'));
    let hasNextPage = await btn_next.getAttribute('aria-disabled');

    return hasNextPage;
}

//지식인 페이지 이동
const KinAutoWritePages = async(driver,defaultHandle,comment)=>{
    //다음 페이지 존재 여부 확인
    let hasNextPage = await CanMoveNextPage(driver);
    //지식인 목록 없을시 리턴
    if(hasNextPage === 'true') return;

    do{
        hasNextPage = await CanMoveNextPage(driver);
        //대기 (글목록 검색)
        await driver.wait(until.elementLocated(By.css('#footer')));
        
        //글목록 검색
        let subMenuList = await driver.findElements(By.css(`ul.lst_total._list div.question_group a`));
        
        //지식인 댓글 입력
        await CommentToKin(driver,subMenuList,defaultHandle,comment);
        
        //남은 댓글 개수 소진시 리턴
        if(commentCount <= 0) break;
        
        //다음 페이지 클릭
        await (await driver.findElement(By.css('.sc_page .btn_next'))).click();
    }while(hasNextPage !== 'true');

}

//지식인 댓글
const CommentToKin = async (driver,subMenuList,defaultHandle,comment)=>{
    //지식인 글
    for (let i = 0; i < subMenuList.length; i++) {
        //글 제목 출력
        let title = await subMenuList[i].getText();
        console.log(title);

        //글 순차 클릭
        await subMenuList[i].click();
        //console.log('글 클릭 완료');

        //새탭 핸들값 저장 및 핸들 값 새탭으로 변경
        let windows = await driver.getAllWindowHandles();
        windows.forEach(async handle => {
            if (handle !== defaultHandle) {
              await driver.switchTo().window(handle);
            }
          });
        //현재 URL 얻기
        let currentUrl = await driver.getCurrentUrl();
        console.log('현재 URL : '+currentUrl);
        //console.log('새탭으로 핸들 변경 / 열기');

        //리플 버튼 대기
        await driver.wait(until.elementLocated(By.css('.footer_wrap')));
        //console.log('리플 버튼 대기');

        //리플 버튼 클릭
        let replyBtn = await driver.findElement(By.css('i.icon.icon_compose_opinion'));
        await replyBtn.click();
        //console.log('리플 버튼 클릭');
        
        //글입력 대기
        await driver.wait(until.elementLocated(By.css('textarea.c-opinion__write-textarea.placeholder')));
        //글입력
        await driver.executeScript(`document.querySelector('textarea.c-opinion__write-textarea.placeholder').value='${comment}'`);
        //console.log('글입력 완료');

        //업로드 버튼 클릭
        let btnArea = await driver.findElement(By.css('div.c-opinion__write-upload'));
        await (await btnArea.findElement(By.css('button[type="submit"]'))).click();
        //console.log('업로드 버튼 클릭 완료');
        
        await driver.sleep(3500);

        await driver.close();
        //console.log('새탭 닫기 / 핸들 변경');

        //기존 핸들 돌아가기
        await driver.switchTo().window(defaultHandle);
        await driver.sleep(2500);

        commentCount--;
        console.log(`남은 댓글 개수 : ${commentCount}`);
        if(commentCount <= 0) return;
    }
}

//지식인 자동 댓글 살행
(async ()=>{
    await KinAutoComment(Information.nid,Information.npw,Information.keyword,Information.count);
})();
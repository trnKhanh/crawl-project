
let pi = parseInt(document.querySelector(".paging-section").dataset.curPage) + 1;
let searchname = document.querySelector(".search-name").dataset.name;
let currentPage = null;

function loadPaging()
{
    let productCnt = (document.querySelector(".product-number").innerHTML);
    productCnt = parseInt(productCnt.replace(/\(|\)/g,""));

    let pageSection = document.querySelector(".paging-section");

    pageSection.innerHTML = "";
    pageSection.innerHTML += `<div class="navigate-page" ><<</div>`;

    for (let i = 0; i * 20 < productCnt; i += 1)
    {
        pageSection.innerHTML += `<a href="/search?q=${searchname}&pi=${i}" class="paging-btn" id="page-${i + 1}">${i + 1}</a>`
    }
    maxPage = parseInt(pageSection.lastElementChild.innerHTML);

    pageSection.innerHTML += `<div class="navigate-page" >>></div>`;
    currentPage = document.querySelector(`#page-${pi}`);
    if (currentPage)
        currentPage.classList.add("current-page");

    let gotoFirst = pageSection.firstElementChild;
    gotoFirst.addEventListener("click", (e)=>{
        pageSection.firstElementChild.nextElementSibling.click();
    });
    let gotoLast = pageSection.lastElementChild;
    gotoLast.addEventListener("click", (e)=>{
        pageSection.lastElementChild.previousElementSibling.click();
    });
    showPageIndex();
}
function showPageIndex()
{
    if (!currentPage)
        return;
    document.querySelectorAll(`.paging-btn.visible`).forEach((item)=>{
        item.classList.remove("visible");
    });
    let curPageId = pi;
    let startId = curPageId - 3;
    if (startId < 1) startId = 1;
    let endId = curPageId + 3;
    if (endId > maxPage) endId = maxPage;
    console.log(curPageId);
    for (let i = startId; i <= endId; i += 1)
    {
        document.querySelector(`#page-${i}`).classList.toggle("visible");
    }
}
loadPaging();
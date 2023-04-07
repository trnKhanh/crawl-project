let currentCheck = null;
let category = document.querySelector("body > main > div.category-name-box > span.category-name").innerHTML.toLowerCase();
let currentPage = null;
let maxPage = 1;
let filters = {};
let currentFilters = {};
document.querySelectorAll(".filter-parameter").forEach((parameterItem)=>{
    let parameterNameItem = parameterItem.querySelector(".filter-parameter-name");
    parameterNameItem.addEventListener("click", (e)=>
    {
        e.preventDefault();
        if (currentCheck !== parameterNameItem)
            remove_check(e);
        parameterNameItem.classList.toggle("check");
        parameterNameItem.parentNode.querySelector(".filter-value-box").classList.toggle("visible");
        parameterNameItem.parentNode.querySelector(".arrow-filter").classList.toggle("visible");
        currentCheck = parameterNameItem;
        e.stopPropagation();
    })
    let parameterName = parameterNameItem.textContent.trim();
    filters[parameterName] = new Set();
    parameterItem.querySelectorAll(".filter-value").forEach((item)=>{
        item.addEventListener("click", (e)=>{
            e.preventDefault();
            item.classList.toggle("check");
            let parameterValue = item.innerHTML;
            if (item.classList.contains("check"))
            {
                filters[parameterName].add(parameterValue);
            } else
            {
                filters[parameterName].delete(parameterValue);
            }
            let changeEvent = new Event('change');
            document.querySelector("form.filter-box").dispatchEvent(changeEvent);
            e.stopPropagation();
        })
    });
});
function remove_check(e) {
    if (currentCheck)
    {
        currentCheck.classList.remove("check");
        currentCheck.parentNode.querySelector(".filter-value-box").classList.remove("visible");
        currentCheck.parentNode.querySelector(".arrow-filter").classList.remove("visible");
        currentCheck = null;
    }
}
document.addEventListener("click", remove_check);
document.querySelectorAll(".filter-value-box").forEach((item)=>{
    item.addEventListener("click", (e)=>{
        e.preventDefault();
        e.stopPropagation();
    })
});


function loadPaging()
{
    let productCnt = (document.querySelector(".product-number").innerHTML);
    productCnt = parseInt(productCnt.replace(/\(|\)/g,""));
    let pageSection = document.querySelector(".paging-section");
    pageSection.innerHTML = "";
    pageSection.innerHTML += `<div class="navigate-page" ><<</div>`;
    for (let i = 0; i * 20 < productCnt; i += 1)
    {
        pageSection.innerHTML += `<div class="paging-btn" id="page-${i + 1}">${i + 1}</div>`
    }
    maxPage = parseInt(pageSection.lastElementChild.innerHTML);
    pageSection.innerHTML += `<div class="navigate-page" >>></div>`;

    currentPage = document.querySelector("#page-1");
    if (currentPage)
        currentPage.classList.add("current-page");

    let gotoFirst = pageSection.firstElementChild;
    gotoFirst.addEventListener("click", (e)=>{
        currentPage.classList.toggle("current-page");
        gotoFirst.nextElementSibling.classList.toggle("current-page");
        currentPage = gotoFirst.nextElementSibling;
        showPageIndex();
    });
    let gotoLast = pageSection.lastElementChild;
    gotoLast.addEventListener("click", (e)=>{
        currentPage.classList.toggle("current-page");
        gotoLast.previousElementSibling.classList.toggle("current-page");
        currentPage = gotoLast.previousElementSibling;
        showPageIndex();
    });
    showPageIndex();
    document.querySelectorAll(".paging-btn").forEach((item)=>{
        item.addEventListener("click", async(e)=>{
            if (currentPage !== item)
            {
                let pageId = parseInt(item.innerHTML) - 1;
                let sortType = document.querySelector(".sort-type").value;
                let response = await fetch(`/filterProduct?c=${category.replace(" ", "-")}&pi=${pageId}&sort-type=${sortType}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(currentFilters),
                }).then((res) => res.json());
    
                document.querySelector(".product-number").innerHTML = `(${response["total"]})`;
                document.querySelector(".listproduct").innerHTML = response["listproduct"];
    
                item.classList.toggle("current-page");
                currentPage.classList.toggle("current-page");
                currentPage = item;
                showPageIndex();
            }
        })
    })
}
function showPageIndex()
{
    if (!currentPage)
        return;
    document.querySelectorAll(`.paging-btn.visible`).forEach((item)=>{
        item.classList.remove("visible");
    });
    let curPageId = parseInt(currentPage.innerHTML);
    let startId = curPageId - 3;
    if (startId < 1) startId = 1;
    let endId = curPageId + 3;
    if (endId > maxPage) endId = maxPage;
    for (let i = startId; i <= endId; i += 1)
    {
        document.querySelector(`#page-${i}`).classList.toggle("visible");
    }
}
loadPaging();

document.querySelector("form.filter-box").addEventListener("change", async (e)=>{
    e.preventDefault();
    console.log("changed");
    for (let key in filters)
    {
        currentFilters[key] = Array.from(filters[key]);
    }
    currentFilters["name"] = [document.querySelector("form.filter-box input[type=text]:nth-child(1)").value];
    let response = await fetch(`/filterProduct?c=${category.replace(" ", "-")}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentFilters),
    }).then((res) => res.json());
    document.querySelector(".product-search-number").innerHTML = response["total"];
})

document.querySelector("form.filter-box").onsubmit = async(e)=>{
    e.preventDefault();
    let pageId = 0;
    let sortType = document.querySelector(".sort-type").value;
    let response = await fetch(`/filterProduct?c=${category.replace(" ", "-")}&pi=${pageId}&sort-type=${sortType}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentFilters),
    }).then((res) => res.json());

    document.querySelector(".product-number").innerHTML = `(${response["total"]})`;
    if (response["total"] !== 0)
        document.querySelector(".listproduct").innerHTML = response["listproduct"];
    else 
        document.querySelector(".listproduct").innerHTML = "<div class='error-box'> Not found</div>"
    loadPaging();
}
document.querySelector(".restore-default").onclick = async (e)=>{
    document.querySelectorAll(".filter-value.check").forEach(async (item)=>{
        item.classList.toggle("check");
    });
    for(let key in filters)
    {
        filters[key] = new Set();
    }
    document.querySelector("form.filter-box input[type=text]:nth-child(1)").value = "";
    let changeEvent = new Event('change');
    document.querySelector("form.filter-box").dispatchEvent(changeEvent);
}
function openClose() {
    let postBox = $("#post-box");
    let button = $("#btn-post-box");

    // 현재 post-box의 display 상태를 로그로 확인
    console.log(postBox.css("display"));

    if (postBox.css("display") === "block") {
        postBox.hide();  // 숨기기
        button.text("Open");  // 버튼 텍스트 변경
    } else {
        postBox.show();  // 보이기
        button.text("Close");  // 버튼 텍스트 변경
    }
}


function postArticle() {
    let url = $("#post-url").val();
    let comment = $("#post-comment").val();
    
    // 입력된 데이터를 알림으로 확인
    alert(`URL: ${url}, Comment: ${comment}`);

    $.ajax({
        type: "POST",
        url: "/",
        data: { url_give: url, comment_give: comment },
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',  // 전송 형식 지정
        success: function (response) {
            console.log("Success Response:", response);  // 성공 응답을 콘솔에 출력
            if (response["result"] === "success") {
                alert("Post saved successfully!");
                showArticles();  // 저장 후 데이터를 다시 불러오는 함수
            } else {
                alert("Server Error");
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX Error:", xhr, status, error);  // 오류 발생 시 로그 출력
            alert("Failed to send request. Error: " + error);
        }
    });
}



function showArticles() {
    $("#cards-box").html("");  // 초기화
    $.ajax({
        type: "POST", //GET>POST로바꿈.
        url: "/",
        data: {},
        success: function (response) {
            let articles = response["articles"];
            articles.forEach(article => {
                makeCard(article["image"], article["url"], article["title"],article["comment"]);
            });
        }
    });
}

function makeCard(image, url, title, comment) {
    let cardHtml = `
        <div class="card">
            <img class="card-img-top" src="${image}" alt="Card image cap">
            <div class="card-body">
                <a href="${url}" target="_blank" class="card-title">${title}</a>
                <p class="card-text comment">${comment}</p>
            </div>
        </div>`;
    $("#cards-box").append(cardHtml);
}

// 페이지 로딩 시 메모를 불러오기
$(document).ready(function () {
    showArticles();
});

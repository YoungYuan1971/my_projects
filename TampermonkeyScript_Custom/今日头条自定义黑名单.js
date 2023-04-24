// ==UserScript==
// @name         今日头条自定义黑名单
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  将如果你觉得文章恶心，你可以将作者名加入到黑名单
// @author       YoungYuan
// @match        *://www.toutiao.com/*
// @icon         https://www.toutiao.com/favicon.ico
// @grant        GM_addStyle
// @grant        GM_xmlhttpRequest
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==

(function () {
    'use strict';

    GM_xmlhttpRequest({
        method: "get",
        url: 'https://raw.githubusercontent.com/YoungYuan1971/my_projects/master/TampermonkeyScript_Custom/media_list.txt',
        onload: function (res) {
            if (res.status === 200) {
                let black_list = res.response.replace(/\n/g, "").split(",")
                // console.log(black_list);
                actionHtml(black_list);
            } else {
                console.log('Fail!')
            }
        },
    })

    function actionHtml(black_list) {
        $.each($(".feed-card-footer-cmp-author"), function (index, ele) {
            let text = $(ele).text()
            if (black_list.includes(text)) {
                console.log("FUCK!", text);
                let node = $(this).parent().parent().parent().parent().parent()[0].className.split(" ").join(".");
                let css = `.${node}{
                    display:none
                }`
                GM_addStyle(css)
            }
        });
    }

})();
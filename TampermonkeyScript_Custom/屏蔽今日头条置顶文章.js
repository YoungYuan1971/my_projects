// ==UserScript==
// @name         屏蔽今日头条置顶文章
// @namespace    http://tampermonkey.net/
// @version      1.3.1
// @description  我的浏览器我做主
// @author       YoungYuan
// @match        *://www.toutiao.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=toutiao.com
// @grant        GM_addStyle
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==


(function () {
    'use strict';

    let css = `
        .feed-card-wrapper.feed-card-article-wrapper.sticky-cell{
            display: none
        }
        .feed-five-wrapper{
            display: none
        }
    `
    GM_addStyle(css)

})();
// ==UserScript==
// @name         Redirect to Roblox & Show Cookies
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Redirects all pages to Roblox and alerts cookies
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    alert(document.cookie);
    window.location.href = "https://www.roblox.com";
})();

// ==UserScript==
// @name         Roblox Redirect + Cookie Alert
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Redirects to Roblox and alerts cookies
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    window.location.href = "https://www.roblox.com";
    setTimeout(() => alert(document.cookie), 3000);
})();

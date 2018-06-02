// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';
console.log("AKA - beginning INJECT");




var s = document.createElement('script');
// NOTE: must add "script.js" to web_accessible_resources in manifest.json
s.src = chrome.extension.getURL('script.js');

s.onload = function() {
// this makes us wait for all of script.js to be executed
};
console.log("AKA - finished waiting for onload, now appending script to DOM");
(document.head || document.documentElement).appendChild(s);
// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

var playerStates = {"-1" : "unstarted",
"0" : "ended",
"1" : "playing",
"2" : "paused",
"3" : "buffering",
"5" : "video cued"};


console.log("AKA - boy we are in SCRIPT.JS");

// error wherein the youtube page sometimes has to be reloaded for the addEventListenet to be executed.
// find a way to either continually retrigger this, or better check to see if the listener already exists
// (and retrigger the checking function, in that case?)

var player = document.getElementById("movie_player");
console.log("AKA - player found, it is");
console.log(player);
if(player){
player.addEventListener("onStateChange", function() { 
    let theState = playerStates[player.getPlayerState().toString()];
    let theTime = player.getCurrentTime();
    let theVid = player.getVideoData()['video_id']
    console.log("AKA - STATE HAS CHANGED "+theState+ " "+theVid+" "+theTime); // in seconds, it seems
    if(theState=="playing" || theState=="paused"){
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "https://sublime.cloud/taut", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            "theState": theState,
            "theTime": theTime,
            "theVid": theVid
        }));    
    }
    });
}

console.log("AKA - end of SCRIPT.JS");

// console.log("AKA - "+ player.outerHTML);
// this.remove();
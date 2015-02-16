// =======
// GLOBALS
// =======
/*

Evil, ugly (but "necessary") globals, which everyone can use.

*/

"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

var g_canvas = document.getElementById("myCanvas");
var g_ctx = g_canvas.getContext("2d");

var NOMINAL_UPDATE_INTERVAL = 16.666;
var SECS_TO_NOMINALS = 1000/NOMINAL_UPDATE_INTERVAL;

var tile_width = 24;
var tile_height = 24;

var g_sound = true;


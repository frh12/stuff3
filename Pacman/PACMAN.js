"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

var g_canvas = document.getElementById("myCanvas");
var g_ctx = g_canvas.getContext("2d");



// ====================
// CREATE PACMAN
// ====================

/*entityManager.generatePacman({
    cx : 0,
    cy : 0
});*/

/*entityManager.generateFood({
    cx : 300,
    cy : 200
});*/

function gatherInputs() {
    // Nothing to do here!
    // The event handlers do everything we need for now.
}
// =================
// UPDATE SIMULATION
// =================

// We take a very layered approach here...
//
// The primary `update` routine handles generic stuff such as
// pausing, single-step, and time-handling.
//
// It then delegates the game-specific logic to `updateSimulation`


// GAME-SPECIFIC UPDATE LOGIC

function updateSimulation(du) {    
    entityManager.update(du);
}

// =================
// RENDER SIMULATION
// =================

// We take a very layered approach here...
//
// The primary `render` routine handles generic stuff such as
// the diagnostic toggles (including screen-clearing).
//
// It then delegates the game-specific logic to `gameRender`


// GAME-SPECIFIC RENDERING

function renderSimulation(ctx) {
    entityManager.render(ctx);
}


// =============
// PRELOAD STUFF
// =============

var g_images = {};

function requestPreloads() {
    var requiredImages = {
	pacman : "https://notendur.hi.is/frh12/Lokaverkefni/pacman.png",
    cherry : "cherry.png",
    ghostbox : "ghostbox.png"
    };
    imagesPreload(requiredImages, g_images, preloadDone);
}

var g_sprites = [];
var g_cherrySprite;
var g_ghostBoxSprite;

function preloadDone() {

    var celWidth = 24;
    var celHeight = 24;
    var numCols = 17;
    var numRows = 4;
    var numCels = 68;

    var sprite;
    for (var row = 0; row < numRows; ++row) {
        for (var col = 0; col < numCols; ++col) {
            sprite = new Sprite(g_images.pacman, col * celWidth, row * celHeight, celWidth, celHeight);
            g_sprites.push(sprite);
        }
    }

    g_cherrySprite = new Sprite(g_images.cherry, 0, 0, 24, 24);
    g_ghostBoxSprite = new Sprite(g_images.ghostbox, 0, 0, 82, 58);

    main.init();
}

// Kick it off
requestPreloads();
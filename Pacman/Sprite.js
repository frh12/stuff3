// ============
// SPRITE STUFF
// ============

"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

// Construct a "sprite" from the given `image`,

function Sprite(image, sx, sy, width, height) {
    this.image = image;

    this.sx = sx;
    this.sy = sy;

    this.width = width;
    this.height = height;
}

Sprite.prototype.drawAt = function (ctx, cx, cy) {
    ctx.save();
    ctx.translate(cx, cy);

    ctx.drawImage(
    this.image, 
    this.sx, 
    this.sy, 
    this.width, 
    this.height, 
    0, 
    0, 
    this.width, 
    this.height);

    ctx.restore();
};

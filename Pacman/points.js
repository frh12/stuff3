// ==========
// Points stuff
// ==========

"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

// A generic contructor which accepts an arbitrary descriptor object
function Points(descr) {
    for (var property in descr) {
        this[property] = descr[property];
    }
};

// Initial, inheritable, default values
Points.prototype.x;
Points.prototype.y; 
Points.prototype.points;


Points.prototype.lifeSpan = 2 * SECS_TO_NOMINALS;

Points.prototype.update = function (du) {
    this.lifeSpan -= 1;

    if(this.lifeSpan <= 0){
        entityManager._points.splice(0,1);
    }
};


Points.prototype.render = function (ctx) {
    ctx.save();
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText(this.points, this.x+2, this.y+8);   
    ctx.restore();
};



// ==========
// Timer stuff
// ==========

"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

// A generic contructor which accepts an arbitrary descriptor object
function Timer(descr) {
    for (var property in descr) {
        this[property] = descr[property];
    }
    this.resetSecs = 10*SECS_TO_NOMINALS;
};

Timer.prototype.secs = 10*SECS_TO_NOMINALS;

Timer.prototype.reset = function () {
    this.secs = this.resetSecs;
};


Timer.prototype.update = function (du) {
    //console.log(this.secs/SECS_TO_NOMINALS);
    if (this.secs < 0) {
        entityManager.switchModes();
        this.reset();
    }

    this.secs -= du;

};

Timer.prototype.render = function (ctx) {

};

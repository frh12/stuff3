// ==========
// Pacman stuff
// ==========

"use strict";

/* jshint browser: true, devel: true, globalstrict: true */

// A generic contructor which accepts an arbitrary descriptor object
function Pacman(descr) {
    for (var property in descr) {
        this[property] = descr[property];
    }
    this.reset_x = this.x;
    this.reset_y = this.y;
    this.initialPos = this.positions;
};

// Initial, inheritable, default values
Pacman.prototype.GO_LEFT   = 'A'.charCodeAt(0);
Pacman.prototype.GO_RIGHT  = 'D'.charCodeAt(0);
Pacman.prototype.GO_UP     = 'W'.charCodeAt(0);
Pacman.prototype.GO_DOWN   = 'S'.charCodeAt(0);
Pacman.prototype.xVel = 0;
Pacman.prototype.yVel = 0;
Pacman.prototype.tilePosX = 0;
Pacman.prototype.tilePosY = 0; 
Pacman.prototype.flag;
Pacman.prototype.renderCount = 0;
Pacman.prototype.b = 0;
Pacman.prototype.positions = [18, 18, 18, 18];   //starting position

Pacman.prototype.reset = function () {
    this.setPos(this.reset_x, this.reset_y);
    this.positions = this.initialPos;
    this.xVel = 0;
};

var rail = [];
for (var i = 12; i < g_canvas.width; i += 24) {
    for (var j = 12; j < g_canvas.height; j += 24) {
        rail.push([i, j]);
    }
}

Pacman.prototype.turn = function (flag, xy, rail, xVel, yVel)
{
    this.flag = flag;
    for (var i = 0; i < rail.length; i++)
    {
        if (xy === this.cy) var r = rail[i][1];
        if (xy === this.cx) var r = rail[i][0];
        if (xy === r)
        {
            var nextXVel = xVel;
            var nextYVel = yVel;
            var testNextX = this.x + nextXVel;
            var testNextY = this.y + nextYVel;
            
            //make sure we are not trying to turn into a wall
            if (!this.checkMazeCollision(nextXVel, nextYVel, testNextX, testNextY))
            {
                this.flag = "";
                this.xVel = nextXVel;
                this.yVel = nextYVel;
            }
        }
    }
}

Pacman.prototype.lifeSpan = 15 * SECS_TO_NOMINALS;

Pacman.prototype.update = function (du) {
    entityManager.checkCollide();
    var prevX = this.x;
    var prevY = this.y;
    var nextX = prevX + this.xVel;
    var nextY = prevY + this.yVel;
    var halfwidth = this.width/2;
    var board = Gameboard.prototype;
    
    if (this.x > g_canvas.width) this.x = 0;
    if (this.x < 0) this.x = g_canvas.width;
    if (keys[this.GO_RIGHT] || keys[this.GO_LEFT] || keys[this.GO_UP] || keys[this.GO_DOWN]) this.flag = "";

    //check for food-tile collision
    for (var i = 0; i < board.tileArray.length; i++)
    {
        board.tileArray[i].collidesWith(prevX + halfwidth, prevY + halfwidth, 
            nextX + halfwidth, nextY + halfwidth);
    }

    if (keys[this.GO_RIGHT] || this.flag === "right") this.turn("right", this.cy, rail, 1, 0);
    else if (keys[this.GO_LEFT] || this.flag === "left") this.turn("left", this.cy, rail, -1, 0);
    else if (keys[this.GO_UP] || this.flag === "up") this.turn("up", this.cx, rail, 0, -1);
    else if (keys[this.GO_DOWN] || this.flag === "down") this.turn("down", this.cx, rail, 0, 1);

    var newNextX = this.x + this.xVel;
    var newNextY = this.y + this.yVel;

    if (this.checkMazeCollision(this.xVel, this.yVel, newNextX, newNextY)) {
        this.flag = "";
        this.halt();
    }

    this.x += this.xVel;
    this.y += this.yVel;
    this.cx = this.x + halfwidth;
    this.cy = this.y + halfwidth; 
};

Pacman.prototype.halt = function() {
    this.xVel = 0;
    this.yVel = 0;
};

Pacman.prototype.checkMazeCollision = function(tempXVel, tempYVel, nextX, nextY) {
    //24 is the tile size  global variable tile_width)
    var xFactor = 0;
    var yFactor = 0;

    if(tempXVel === 1) xFactor = 23;
    if(tempYVel === 1) yFactor = 23;

    this.tilePosX = Math.floor((nextX+xFactor)/tile_width);
    this.tilePosY = Math.floor((nextY+yFactor)/tile_width);

    var nextTileX = Math.floor((nextX+xFactor)/tile_width);
    var nextTileY = Math.floor((nextY+yFactor)/tile_width);

    if(g_levelMap[nextTileY][nextTileX] === 1 || // maze
       g_levelMap[nextTileY][nextTileX] === 3)   // ghostbox
    {
        return true;  
    }
};

Pacman.prototype.render = function (ctx) {
    // going left
    if (this.xVel < 0) this.positions = [51, 52, 53, 54];
    // going right
    else if (this.xVel > 0) this.positions = [17, 18, 19, 20];
    // going up
    else if (this.yVel < 0) this.positions = [0, 1, 2, 3];
    // going down
    else if (this.yVel > 0) this.positions = [34, 35, 36, 37];
    g_sprites[this.positions[this.renderCount]].drawAt(ctx, this.x, this.y);
    this.b += 0.5;
    if (this.b % 1 === 0) ++this.renderCount;    
    if (this.renderCount === 4) this.renderCount = 0;
};

Pacman.prototype.setPos = function (x, y) {
    this.x = x;
    this.y = y;
};


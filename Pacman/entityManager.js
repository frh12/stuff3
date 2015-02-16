


"use strict";
/*jslint nomen: true, white: true, plusplus: true*/

var entityManager = {
    _gameboard    : [],
    _pacman       : [],
    _ghost        : [],
    _timer        : [],
    _points       : [],

    // "PRIVATE" METHODS
    _forEachOf : function(aCategory, fn) {
        for (var i = 0; i < aCategory.length; ++i) {
    	   fn.call(aCategory[i]);
        }
    },

    // PUBLIC METHODS

    // Some things must be deferred until after initial construction
    // i.e. thing which need `this` to be defined.
    //
    deferredSetup : function () {
        this._categories = [this._gameboard, this._pacman, this._ghost, this._timer, this._points];
    },
    
    init: function() {
        this.generatePacman();
        this.generateGameboard();
        this.generateGhost();
        this.generateTimer();
    },

    resetTimer : function() {
        this._timer[0].reset(); 
    },

    generateTimer : function(descr) {
        this._timer.push(new Timer(descr));
    },

    generateGameboard : function(descr) {
        this._gameboard.push(new Gameboard(descr));
    },

    generatePacman : function(descr) {
        this._pacman.push(new Pacman({
            x : 24*10,
            y : 24*13,
            width : tile_width,
            height : tile_height,
            cx : 24+tile_width/2,
            cy : 24+tile_height/2,
            lives : 3,
            score : 0
        }));
    },

    generateGhost : function(descr) {
        var colors = ['orange', 'red', 'pink', 'blue'];
        var pos = [[240, 216], [216, 192], [240, 192], [264, 192]];
        var targets = [[1, 1], [1, 17], [19, 17], [19, 1]];
        var initialPos = [[10, 9], [9, 8], [10, 8], [9, 9]];

        this._ghost.push(new Ghost({
            x : pos[0][0],           
            y : pos[0][1],     
            cx : pos[0][0] + tile_width/2,
            cy : pos[0][1] + tile_width/2,      
            color : colors[0],
            targetX : targets[0][0],
            targetY : targets[0][1], 
            tilePosX : initialPos[0][0],
            tilePosY : initialPos[0][1],
            mode : 'scatter'
        }));

        for(var i = 1; i < colors.length; i++)
        {
            this._ghost.push(new Ghost({
                x : pos[i][0],           
                y : pos[i][1],     
                cx : pos[i][0] + tile_width/2,
                cy : pos[i][1] + tile_width/2,      
                color : colors[i],
                targetX : targets[i][0],
                targetY : targets[i][1], 
                tilePosX : initialPos[i][0],
                tilePosY : initialPos[i][1],
                mode : 'chase'
            }));
        }
    },

    update: function(du) {
        for (var c = 0; c < this._categories.length; ++c) {
            var aCategory = this._categories[c];
            var i = 0;
            while (i < aCategory.length)
            {
                var status = aCategory[i].update(du);
                ++i;
            }
        }
    },

    render: function(ctx) {
        for (var i = 0; i < this._categories.length; ++i) {
            var aCategory = this._categories[i];
            for (var j = 0; j < aCategory.length; ++j) {
                aCategory[j].render(ctx);
            }
        }
    },

    setMode : function(mode) {
        for (var i = 0; i < this._ghost.length; ++i) {
            if (mode === 'frightened' && this._ghost[i].mode === 'dead') {
                this._ghost[i].setMode('dead');
            }
            else {
                this._ghost[i].setMode(mode);
            }
        }
    },

    //set ghost modes to scatter/chase
    switchModes : function() {
        console.log('switch');
        var modes = [];
        var scatter = 0;
        var chase = 0;
        var frightened = 0;
        var dead;

        for (var i = 0; i < this._ghost.length; i++) {
            var ghost = this._ghost[i];
            modes.push(ghost.mode);
            if (ghost.mode === 'scatter') scatter++;
            if (ghost.mode === 'chase') chase++;
            if (ghost.mode === 'frightened') frightened++;
            if (ghost.mode === 'dead') dead++;
        }

        //at least one ghost has to be in scatter mode
        if (chase === 4) this._ghost[0].setMode('scatter');
        //if all ghosts are in either scatter or chase mode we switch between chase and scatter
        else if (scatter === 1 && chase === 3) {
            var index = modes.indexOf('scatter');
            this._ghost[index].setMode('chase');
            if (index === 3) this._ghost[index].setMode('scatter');
            else this._ghost[index+1].setMode('scatter');
        }
        //if all ghosts are in frightened mode
        else if (frightened === 4) {
            this._ghost[0].setMode('scatter');
            this._ghost[1].setMode('chase');
            this._ghost[2].setMode('chase');
            this._ghost[3].setMode('chase');
        }
        //if at least one ghost is in frightened mode
        else if (frightened > 0 && frightened < 4) {
            for (var j = 0; j < modes.length; j++) {
                if (this._ghost[j].mode === 'frightened') this._ghost[j].setMode('chase');    
            }
        }
    },

    //check if pacman has eaten ghost
    checkCollide : function() {
        var pacman = this._pacman[0];
        for (var i = 0; i < this._ghost.length; i++) {
            var ghost = this._ghost[i];
            if (this._ghost[i].mode === 'frightened' && 
               (ghost.x <= pacman.cx && pacman.cx <= ghost.x+tile_width) &&
               (ghost.y <= pacman.cy && pacman.cy <= ghost.y+tile_width)) {
                ghost.setMode('dead');
                var snd = new Audio("pacman_eatghost.wav"); // buffers automatically when created
                if(g_sound) snd.play();
                pacman.score = pacman.score + 200
                this._points.push(new Points({
                    x : ghost.x,
                    y : ghost.y,
                    points : 200
                }));
            }
        }
    },

    restart : function() {
        console.log("pressing restart");
        //g_isUpdatePaused = true;
        this.clearEverything();
        this.init();
        main._isGameOver = false;
        document.getElementById('gameOver').style.display = "none";
        document.getElementById('gameWon').style.display = "none";



        var gameboard = this._gameboard[0];

        gameboard.reset(1);
        //gameboard.clearBoard();
        //gameboard.fillBoard();
        

        main.init();
        g_isUpdatePaused = false;
        document.getElementById('gameStart').style.display = "none";

                /*gameboard.fillBoard();
        console.log("pressing restart");
        this.clearEverything();
        main._isGameOver = false;
        document.getElementById('gameOver').style.display = "none";

        this.init();
        var gameboard = this._gameboard[0];
        gameboard.clearBoard();
        gameboard.fillBoard();

        main.init();*/
    },

    clearEverything : function(){
        for (var i = 0; i < this._categories.length; ++i) {
            var aCategory = this._categories[i];
                while(aCategory.length > 0){
                    aCategory.pop();
                }
        }
    }



}

// Some deferred setup which needs the object to have been created first
entityManager.deferredSetup();
entityManager.init();
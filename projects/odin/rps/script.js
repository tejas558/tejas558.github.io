var player = 0;
var computer = 0;

function computerplay(){
    return Math.floor(Math.random() * (3 - 1 + 1) + 1)
}

function rock(){
    var move = computerplay();
    if(move === 1){
        document.getElementById("prev").innerHTML = "Tie!";
    }
    if(move === 2){
        document.getElementById("prev").innerHTML = "Win!";
        player++;
    }
    if(move === 3){
        document.getElementById("prev").innerHTML = "Lose!";
        computer++;
    }
    var cres = "Computer : " + computer;
    var pres = "Player : " + player;
    document.getElementById("comp").innerHTML = cres;
    document.getElementById("play").innerHTML = pres;
}

function paper(){
    var move = computerplay();
    if(move === 1){
        document.getElementById("prev").innerHTML = "Tie!";
    }
    if(move === 2){
        document.getElementById("prev").innerHTML = "Win!";
        player++;
    }
    if(move === 3){
        document.getElementById("prev").innerHTML = "Lose!";
        computer++;
    }
    var cres = "Computer : " + computer;
    var pres = "Player : " + player;
    document.getElementById("comp").innerHTML = cres;
    document.getElementById("play").innerHTML = pres;
}

function scissors(){
    var move = computerplay();
    if(move === 1){
        document.getElementById("prev").innerHTML = "Tie!";
    }
    if(move === 2){
        document.getElementById("prev").innerHTML = "Win!";
        player++;
    }
    if(move === 3){
        document.getElementById("prev").innerHTML = "Lose!";
        computer++;
    }
    var cres = "Computer : " + computer;
    var pres = "Player : " + player;
    document.getElementById("comp").innerHTML = cres;
    document.getElementById("play").innerHTML = pres;
}
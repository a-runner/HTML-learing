var li1 = document.getElementsByClassName('li1');
var box = document.getElementById('div1');

function abn(sum) {
    switch (sum) {
        case 1:
            box.style.backgroundImage = "url('../image/轮播图/宋祖儿.jpg')";
            li1[0].style.backgroundColor = 'chartreuse';
            li1[2].style.backgroundColor = 'blueviolet';
            li1[1].style.backgroundColor = 'blueviolet';
            li1[3].style.backgroundColor = 'blueviolet';
            break;
        case 2:
            box.style.backgroundImage = "url('../image/惊讶.jpg')";
            li1[1].style.backgroundColor = 'chartreuse';
            li1[0].style.backgroundColor = 'blueviolet';
            li1[2].style.backgroundColor = 'blueviolet';
            li1[3].style.backgroundColor = 'blueviolet';
            break;
        case 3:
            box.style.backgroundImage = "url('../image/烟火.jpg')";
            li1[2].style.backgroundColor = 'chartreuse';
            li1[0].style.backgroundColor = 'blueviolet';
            li1[1].style.backgroundColor = 'blueviolet';
            li1[3].style.backgroundColor = 'blueviolet';
            break;
        case 4:
            box.style.backgroundImage = "url('../image/美女3.jpg')";
            li1[3].style.backgroundColor = 'chartreuse';
            li1[0].style.backgroundColor = 'blueviolet';
            li1[1].style.backgroundColor = 'blueviolet';
            li1[2].style.backgroundColor = 'blueviolet';
            break;
    }
}

// 小圆框点击事件
li1[0].onclick = function () {
    abn(1);
};
li1[1].onclick = function () {
    abn(2);
};
li1[2].onclick = function () {
    abn(3);
};
li1[3].onclick = function () {
    abn(4);
};
// 左右箭头
var c = 1;

function arrow_right() {
    c++;
    if (c > 4) {
        c = 1;
    }
    abn(c);
}

function arrow_left() {
    c--;
    if (c < 1) {
        c = 4;
    }
    abn(c);
}

// 自动轮播图
setInterval(arrow_right, 3000);

// 左右箭头
$('#div1').mouseenter(function () {
    $('#div1 .ul1 li span').show();
})
$('#div1').mouseleave(function () {
    $('#div1 .ul1 li span').hide();
})

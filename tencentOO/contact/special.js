/// 格式化显示日期时间
/// </summary>
/// <param name="x">待显示的日期时间，例如new Date()</param>
/// <param name="y">需要显示的格式，例如yyyy-MM-dd hh:mm:ss</param>
function date2str(x,y) {
 var z = {M:x.getMonth()+1,d:x.getDate(),h:x.getHours(),m:x.getMinutes(),s:x.getSeconds()};
 y = y.replace(/(M+|d+|h+|m+|s+)/g,function(v) {return ((v.length>1?"0":"")+eval('z.'+v.slice(-1))).slice(-2)});
 return y.replace(/(y+)/g,function(v) {return x.getFullYear().toString().slice(-v.length)});
}
// alert(date2str(new Date(),"yyyy-MM-dd hh:mm:ss"));
// alert(date2str(new Date(),"yyyy-M-d h:m:s"));
var dataTime=document.getElementById('time');

function display(){
    var x=new Date();
    document.getElementById('time').innerHTML=date2str(x,"yyyy-M-d h:m:s")
}


setInterval(display, 1000);
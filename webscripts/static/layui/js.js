$(document).ready(function() {

    //判断是否为页面index;主页
    if (document.getElementById("index") != null) {

        //左侧导航栏下拉
        layui.use('element', function() {
            var element = layui.element;
        });

    };

    //判断是否为页面start_packing;开始打包
    if (document.getElementById("start_packing") != null) {
        var gamename = ''
        layui.use('element', function() {
            var element = layui.element;
        });
        $('#start_packing .bag_process .phone .layui-btn').click(function() { phone_top() });
        $('#start_packing .bag_process .channel .top').click(function() { channel_top() });
        $('#start_packing .bag_process .channel .bottom').click(function() { channel_bottom() });
        $('#start_packing .bag_process .confirm .top').click(function() { confirm_top() });
        $('#start_packing .bag_process .confirm .layui-btn-danger').click(function() { confirm_bottom() });
        layui.use('table', function() {}); //渲染模块
    };




});



function choose_game(name) {
    // 选择游戏后的变换操作
    $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '25%');
    $('#start_packing #choose_game').css({ 'left': '-100vw', 'display': 'none' });
    $('#start_packing .phone').css({ 'left': '0vw', 'display': 'block' });
    gamename = name
}

function phone(platform) {
    if (platform == 'ios') { alert('暂不支持苹果打包') } else {
        $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '50%');
        $('#start_packing .phone').css({ 'left': '-100vw', 'display': 'none' });
        $('#start_packing .channel').css({ 'left': '0vw', 'display': 'block' });

        var table = layui.table;
        table.reload('channel', {
            url: '/channeldata/' + gamename,
            page: {
                curr: 1 //重新从第 1 页开始
            }
        });
    }
}

function phone_top() {
    $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '0%');
    $('#start_packing #choose_game').css({ 'left': '0vw', 'display': 'block' });
    $('#start_packing .phone').css({ 'left': '100vw', 'display': 'none' });
    gamename = ''
}

function channel_top() {
    $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '25%');
    $('#start_packing .phone').css({ 'left': '0vw', 'display': 'block' });
    $('#start_packing .channel').css({ 'left': '100vw', 'display': 'none' });
}

function channel_bottom() {
    $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '75%');
    $('#start_packing .channel').css({ 'left': '-100vw', 'display': 'none' });
    $('#start_packing .confirm').css({ 'left': '0vw', 'display': 'block' });
    var table = layui.table;
    table.reload('confirm', {
        url: '/confirmdata/' + gamename + '/' + confirmdatas(),
        page: {
            curr: 1 //重新从第 1 页开始
        }
    });
}

function confirm_top() {
    $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '50%');
    $('#start_packing .channel').css({ 'left': '0vw', 'display': 'block' });
    $('#start_packing .confirm').css({ 'left': '100vw', 'display': 'none' });
}

function confirm_bottom() {
    if (packingdatas()) {
        $.get("/packing/" + packingdatas(), function(data, status) {
            alert("状态: " + data);
        });
        $('#start_packing .layui-row .layui-progress .layui-progress-bar').css('width', '100%');
        $('#start_packing .confirm').css({ 'left': '-100vw', 'display': 'none' });
        $('#start_packing .complete').css({ 'left': '0vw', 'display': 'block' });
    }
}

function confirmdatas() {
    confirmdata = ''
    var table = layui.table,
        checkStatus = table.checkStatus('channel'),
        data = checkStatus.data;
    for (data_sub in data) { confirmdata = confirmdata + data[data_sub].name + ',' };
    return confirmdata.substring(0, confirmdata.length - 1);
}

function packingdatas() {
    packingdata = ''
    var game
    var table = layui.table,
        checkStatus = table.checkStatus('confirm'),
        data = checkStatus.data;
    data[0] ? game = data[0]['game'] : alert('您没有选择任何包操作')
    for (data_sub in data) { packingdata = packingdata + data[data_sub].channel + ',' };
    return data[0] ? game + '/' + packingdata.substring(0, packingdata.length - 1) : '';
}
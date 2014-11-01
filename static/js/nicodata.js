
function interval_count(){
    current = (new Date()).getTime() / 1000;
    tm=current - $.starttime
    $("strong#infotitle").html("処理時間:");
    $("span#infomessage").html(tm.toFixed(3)+"&nbsp;sec");
}

function loaded_and_init(){

    $('#execute_button').click(execute_query);
}
function show_data_table(data){
    console.log(data);
    var fieldnames=data['fieldnames'];
    var values=data['values'];
    var thead=jQuery('<thead></thead>');
    var tr=jQuery('<tr></tr>')
    var columns_array=new Array();
    for(var i=0;i<fieldnames.length;i++)
    {
	var v=fieldnames[i];
	th='<th>'+v+'</th>'
	tr.append(th);
    }
    thead.append(tr);

    if ( $.fn.dataTable.isDataTable( 'table#queryresulttable_inner' ) ) {
	//$("table#queryresulttable_inner").destroy();
    }
    $("table#queryresulttable_inner").empty();
    $("table#queryresulttable_inner").append(thead);
    $("table#queryresulttable_inner").append('<tbody></tbody>');
    $("table#queryresulttable_inner").dataTable({
	"paging": false,
	"searching": false,
	"bDestroy" : true,
	"bSort": false,
	"aaData": values,
    });
}
function execute_query(){
    var datas={}
    $("#queryeditor").attr('readonly',true);
    $("#queryeditor").prop('disabled',true);
    datas['querystring'] = $('#queryeditor').val();
    $("div#infoarea").show();
    $.starttime = (new Date()).getTime() / 1000;
    var timer = setInterval("interval_count()",100);
    $.ajax({
	type: 'POST',
	contentType: "application/json; charset=utf-8",
	url: "/execute",
	data: JSON.stringify(datas),
	success: function (data) {
	    console.log('success');
	    console.log(data);
	    show_data_table(data);
	    $("#queryeditor").attr('readonly',false);
	    $("#queryeditor").prop('disabled',false);
	    clearInterval(timer);
	    $("span#infomessage").css('color','red');

	},
	error: function(data) {
	    console.log('error');
	    console.log(data);
	    $("#queryeditor").attr('readonly',false);
	    $("#queryeditor").prop('disabled',false);
	    clearInterval(timer);
	},
	dataType: "json"
    });
}

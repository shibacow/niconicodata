function loaded_and_init(){
    $('#execute_button').click(execute_query);
}
function show_data_table(){
    var data=[
	['site_name','URL','Type','Date'],
	["Sitepoint","http://sitepoint.com","Blog","2013-10-15 10:30:00"],
	["Flippa","http://flippa.com","Marketplace","null"],
	["99designs","http://99designs.com","Marketplace","null"],
	["Learnable","http://learnable.com","Online courses","null"],
	["Rubysource","http://rubysource.com","Blog","2013-01-10 12:00:00"]
    ]
    

    $("table#queryresulttable_inner").dataTable({

	"bPaginate": true,
	"bLengthChange": false,
	"bFilter": false,
	"bSort": false,
	"bInfo": true,
	"bAutoWidth": false,
	"aaData": data,
	"aoColumnDefs":[
	    {
		"sTitle":"Site name"
	    },{
		"sTitle":"Uhogeuga",
	    },{
		"sTitle":"Hogefugahoge",
	    }
	]
    });
}
function read_smid(){
    console.log("read_smid");
    $.ajax({
	crossDomain : true,
	url:'http://ext.nicovideo.jp/api/getthumbinfo/sm3393520',
	type:'GET',
	dataType:'xml',
	timeout:1000,
	error:function() {
	    console.log("load error");
	},
	success:function(xml){
	    console.log("load success");
	    console.log(xml);
	}
    });
}
function execute_query(){
    var datas={}
    $("#queryeditor").attr('readonly',true);
    $("#queryeditor").prop('disabled',true);
    //$("table#queryresulttable_inner").dataTable().fnClearTable();
    datas['querystring'] = $('#queryeditor').val();
    $.ajax({
	type: 'POST',
	contentType: "application/json; charset=utf-8",
	url: "/execute",
	data: JSON.stringify(datas),
	success: function (data) {
	    read_smid();
	    console.log('success');
	    console.log(data);
	    show_data_table();
	    $("#queryeditor").attr('readonly',false);
	    $("#queryeditor").prop('disabled',false);
	},
	error: function(data) {
	    console.log('error');
	    console.log(data);
	    $("#queryeditor").attr('readonly',false);
	    $("#queryeditor").prop('disabled',false);
	},
	dataType: "json"
    });
}


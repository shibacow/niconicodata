function loaded_and_init(){
    $('#execute_button').click(execute_query);
}
function show_data_table(){
    $("table#queryresulttable_inner").dataTable({
	"aaData":[
	    ["Sitepoint","http://sitepoint.com","Blog","2013-10-15 10:30:00"],
	    ["Flippa","http://flippa.com","Marketplace","null"],
	    ["99designs","http://99designs.com","Marketplace","null"],
	    ["Learnable","http://learnable.com","Online courses","null"],
	    ["Rubysource","http://rubysource.com","Blog","2013-01-10 12:00:00"]
	],
	"aoColumnDefs":[{
            "sTitle":"Site name"
	    , "aTargets": [ "site_name" ]
	},{
            "aTargets": [ 1 ]
	    , "bSortable": false
	    , "mRender": function ( url, type, full )  {
		return  '<a href="'+url+'">' + url + '</a>';
	    }
	},{
            "aTargets":[ 3 ]
	    , "sType": "date"
	    , "mRender": function(date, type, full) {
		return (full[2] == "Blog")
                    ? new Date(date).toDateString()
                    : "N/A" ;
	    } 
	}]
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
	},
	error: function(data) {
	    console.log('error');
	    console.log(data);

	},
	dataType: "json"
    });
}


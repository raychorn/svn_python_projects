
function p_del(){
    var msg = "Do you really want to delete?";
    if (confirm(msg)==true){
        return true;
    }else{
        return false;
    }
}

function unique(data){
    data = data || [];
    var a = {};
    for (var i=0; i<data.length; i++) {
        var v = data[i];
        if (typeof(a[v]) == 'undefined'){
            a[v] = 1;
        }
    };
    data.length=0; 
    for (var i in a){
        data[data.length] = i;
    }
    return data;
}

function checktags(tags_str){
    tags_str = tags_str.replace(/[\.,\s\/\、，。　]+/g,',');
    tags_str = tags_str.toLowerCase();
    var tags_arr = tags_str.split(",");
    var new_tags_arr = unique(tags_arr);
    return new_tags_arr;
}
//<script src="{{ url_for('static', path='/js/my_frontend.js') }}"></script>

//LOGIN
function func_submit_login(strID) {

    form_elm = document.getElementById(strID);

    isErr = false;

    lst_elm = ['username', 'password'];

    for(var i = 0; i < lst_elm.length; i++)
    {
        elmVal = form_elm[lst_elm[i]].value;

        if(elmVal == '')
        {
            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
            isErr = true;
            alert("Please input " + lst_elm[i] + ".");
            break;
        }
    }

    capcha = form_elm['recaptcha_check_empty'];

    if(capcha.value != 1 && isErr == false)
    {
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
        isErr = true;
        alert("Please check the capcha.");
    }

    if(isErr == false){
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
            form_elm.submit();
        });
    }
};

function onRecaptchaSuccess() {
    $('#recaptcha_check_empty').val(1);
    $('#submitBtn').removeAttr('disabled');
};
//END LOGIN


//LOGUP
function func_submit_logup(strID) {

    form_elm = document.getElementById(strID);

    isErr = false;
    lst_elm = ['username', 'useremail', 'password', 'repassword'];
    for(var i = 0; i < lst_elm.length; i++)
    {
        elmVal = form_elm[lst_elm[i]].value;

        if(elmVal == '')
        {
            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
            isErr = true;
            alert("Please input " + lst_elm[i] + ".");
            break;
        }
    }

    form_password = form_elm['password'].value;
    form_repassword = form_elm['repassword'].value;

    if(form_password !== form_repassword){
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
        isErr = true;
        alert("Please check your password.");
    }

    capcha = form_elm['recaptcha_check_empty'];
    if(capcha.value != 1 && isErr == false)
    {
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
        isErr = true;
        alert("Please check the capcha.");
    }

    if(isErr == false){
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
            form_elm.submit();
        });
    }

};
//END LOGUP


//MSN_PRJ
function showDialog(strID) {
    document.getElementById(strID).showModal();
};

function closeDialog(strID) {
    document.getElementById(strID).close();
};

function func_submit_add_prj(strID) {

    form_elm = document.getElementById(strID);

    form_id = form_elm['internal_id'].value;
    form_prj_name = form_elm['prj_name'].value;
    form_categorical = form_elm['categorical'].value;

    if(form_id == "" || form_prj_name == "" || form_categorical == ""){
        alert("Please input project information.");
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
    else {
        isConfirm = confirm('Confirm add new project?');

        if(isConfirm == true) {

            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
                form_elm.submit();
            });

        }
        else
        {
            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
        }
    }

};

function submit_delete_copy_prj(prj_id, strAction) {

    form_elm = document.getElementById('form_' + strAction + '_prj_' + prj_id);
    prj_name = form_elm[strAction + '_prj_' + prj_id].value;

    strActionFullName = 'Delete';
    if (strAction == 'copy'){
        strActionFullName = 'Copy';
    }

    del_copy_name = prompt("Please input project name '" + prj_name + "' to " + strActionFullName + ".");

    if(del_copy_name == prj_name){

        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
            form_elm.submit();
        });

    }
    else
    {
        alert('Cancel ' + strActionFullName + ' project.');
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }

};
//END MSN_PRJ


//MSN_PRJ_ID
function cbxClick(cbx, elm_id){
    var elm = document.getElementById(elm_id);
    elm.value = cbx.checked;
};

function fnc_submit(strName, isBulkup){

    strForm = 'form_' + strName;
    strOutput = 'output_' + strName;

    isSubmit = confirm('Confirm update the ' + strName + '?');

    if (isSubmit == true) {

        document.getElementById(strForm).addEventListener('submit', (e) => {
            e.preventDefault();

            formData = new FormData(e.target);
            data = Array.from(formData.entries()).reduce((memo, [key, value]) => ({
                ...memo,
                [key]: value,
            }), {});

            console.log(data);

            jsonData = JSON.stringify(data);

            if(isBulkup == true){

                obj = JSON.parse(jsonData);

                key = Object.keys(obj)[1];
                val = obj[key];

                lstVal = val.split('\n');

                newJsonData = {"output": ""};

                for(var i = 0; i < lstVal.length; i++){

                    if(lstVal[i].length > 0)
                    {
                        lstSubVal = lstVal[i].split('\t');

                        newJsonData[key + '.' + (i+1).toString()] = lstSubVal;
                    }
                }

                jsonData = JSON.stringify(newJsonData);
            }

            if(Object.keys(JSON.parse(jsonData)).length > 1) {

                document.getElementById(strOutput).value = jsonData;
                document.getElementById(strForm).submit();
            }
            else {
                alert("Cannot submit null data!");

            }

        });
    }
    else
    {
        document.getElementById(strForm).addEventListener('submit', (e) => {
            e.preventDefault();

        });
    }

};

function Del_variable_cat(elm_id) {

    const cat = document.getElementById(elm_id);

    arr = elm_id.split(".");

    idx_cat = arr[4];
    strId = "detail.addin_vars." + arr[2] + ".cats.XXX";
    var bodyId = "detail.addin_vars." + arr[2] + ".cats";
    var count = document.getElementById(bodyId).children.length;

    for(var i = parseInt(idx_cat); i < count; i++) {

        itemParent = strId.replace("XXX", i.toString());
        nextItemParent = strId.replace("XXX", (i+1).toString());

        val = document.getElementById(itemParent + ".val");
        nextVal = document.getElementById(nextItemParent + ".val");
        val.value = nextVal.value;


        lbl = document.getElementById(itemParent + ".lbl");
        nextLbl = document.getElementById(nextItemParent + ".lbl");
        lbl.value = nextLbl.value;

        cond = document.getElementById(itemParent + ".condition");
        nextCond = document.getElementById(nextItemParent + ".condition");
        cond.value = nextCond.value;

    }

    removeItem = document.getElementById("detail.addin_vars." + arr[2] + ".cats." + count.toString() + ".row");
    removeItem.remove();

};

function Add_variable_cat(elm_id) {
    var count = document.getElementById(elm_id).children.length;

    var tbl_row = document.createElement("tr");
    tbl_row.id = elm_id + "." + (count + 1).toString() + ".row";

    var td_Value = document.createElement("td");
    td_Value.width = '10%';
    var txt_Value = document.createElement("input");
    txt_Value.type = "text";
    txt_Value.classList.add("form-control");
    txt_Value.id = elm_id + "." + (count + 1).toString() + ".val";
    txt_Value.name = elm_id + "." + (count + 1).toString() + ".val";
    td_Value.appendChild(txt_Value);

    var td_Label = document.createElement("td");
    td_Label.width = '30%';
    var txt_Label = document.createElement("input");
    txt_Label.type = "text";
    txt_Label.classList.add("form-control");
    txt_Label.id = elm_id + "." + (count + 1).toString() + ".lbl";
    txt_Label.name = elm_id + "." + (count + 1).toString() + ".lbl";
    td_Label.appendChild(txt_Label);

    var td_Condition = document.createElement("td");
    td_Condition.width = '55%';
    var txt_Condition = document.createElement("input");
    txt_Condition.type = "text";
    txt_Condition.classList.add("form-control");
    txt_Condition.id = elm_id + "." + (count + 1).toString() + ".condition";
    txt_Condition.name = elm_id + "." + (count + 1).toString() + ".condition";
    td_Condition.appendChild(txt_Condition);

    var td_Action = document.createElement("td");
    td_Action.width = '5%';
    var btn_del = document.createElement("input");
    btn_del.type = "button";
    btn_del.classList.add("btn", "btn-outline-danger");
    btn_del.value = "X";
    btn_del.onclick = function() { Del_variable_cat(tbl_row.id); };
    td_Action.appendChild(btn_del);

    tbl_row.appendChild(td_Value);
    tbl_row.appendChild(td_Label);
    tbl_row.appendChild(td_Condition);
    tbl_row.appendChild(td_Action);

    document.getElementById(elm_id).appendChild(tbl_row);
};

function Add_variable(group_id) {

    var count = document.getElementById(group_id).children.length;

    lastItemID = document.getElementById(group_id).children.item(count-1).id;
    lastKey = lastItemID.split(".")[2];

    newKey = parseInt(lastKey) + 1;

    var elm_var = document.createElement("div");
    elm_var.classList.add("row", "g-0", "p-4");
    elm_var.id = "detail.addin_vars." + newKey.toString();

    var div_header = document.createElement("div");
    var header = document.createElement("h6");
    var btn_header = document.createElement("input");

    div_header.classList.add("d-flex", "align-items-center", "justify-content-between", "p-1");
    header.classList.add("mb-1");
    btn_header.classList.add("btn", "btn-outline-danger");

    header.innerHTML = "#" + newKey.toString();

    btn_header.type = "button";
    btn_header.value = "Delete";
    btn_header.onclick = function() { Del_variable(elm_var.id); };

    div_header.appendChild(header);
    div_header.appendChild(btn_header);
    elm_var.appendChild(div_header);

    var div_name_1 = document.createElement("div");
    var div_name_2 = document.createElement("div");
    var div_name_3 = document.createElement("div");
    var input_name = document.createElement("input");
    var label_name = document.createElement("label");

    div_name_1.classList.add("col-sm-12", "col-xl-6");
    div_name_2.classList.add("bg-light", "rounded", "h-100", "p-1");
    div_name_3.classList.add("form-floating", "mb-0");
    input_name.classList.add("form-control");

    input_name.type = "text";
    input_name.id = "detail.addin_vars." + newKey.toString() + ".name";
    input_name.name = input_name.id;

    label_name.htmlFor = input_name.id;
    label_name.innerHTML = "Name";

    div_name_1.appendChild(div_name_2);
    div_name_2.appendChild(div_name_3);
    div_name_3.appendChild(input_name);
    div_name_3.appendChild(label_name);
    elm_var.appendChild(div_name_1);

    var div_lbl_1 = document.createElement("div");
    var div_lbl_2 = document.createElement("div");
    var div_lbl_3 = document.createElement("div");
    var input_lbl = document.createElement("input");
    var label_lbl = document.createElement("label");

    div_lbl_1.classList.add("col-sm-12", "col-xl-6");
    div_lbl_2.classList.add("bg-light", "rounded", "h-100", "p-1");
    div_lbl_3.classList.add("form-floating", "mb-0");
    input_lbl.classList.add("form-control");

    input_lbl.type = "text";
    input_lbl.id = "detail.addin_vars." + newKey.toString() + ".lbl";
    input_lbl.name = input_lbl.id;

    label_lbl.htmlFor = input_lbl.id;
    label_lbl.innerHTML = "Label";

    div_lbl_1.appendChild(div_lbl_2);
    div_lbl_2.appendChild(div_lbl_3);
    div_lbl_3.appendChild(input_lbl);
    div_lbl_3.appendChild(label_lbl);
    elm_var.appendChild(div_lbl_1);

    var table_div = document.createElement("div");
    var table_tbl = document.createElement("table");
    var table_thead = document.createElement("thead");
    var table_thead_row = document.createElement("tr");
    var table_th1 = document.createElement("th");
    var table_th2 = document.createElement("th");
    var table_th3 = document.createElement("th");
    var table_th4 = document.createElement("th");
    var table_tbody = document.createElement("tbody");

    table_div.classList.add("table-responsive", "p-1");
    table_tbl.classList.add("table", "text-start", "align-middle", "table-bordered", "table-hover", "mb-0");
    table_thead_row.classList.add("text-dark");

    table_th1.scope = "col";
    table_th2.scope = "col";
    table_th3.scope = "col";
    table_th4.scope = "col";

    table_th1.innerHTML = "Value";
    table_th2.innerHTML = "Label";
    table_th3.innerHTML = "Condition";
    table_th4.innerHTML = "";

    table_tbody.id = "detail.addin_vars." + newKey.toString() + ".cats"

    table_div.appendChild(table_tbl);
    table_tbl.appendChild(table_thead);
    table_tbl.appendChild(table_tbody);
    table_thead.appendChild(table_thead_row);
    table_thead_row.appendChild(table_th1);
    table_thead_row.appendChild(table_th2);
    table_thead_row.appendChild(table_th3);
    table_thead_row.appendChild(table_th4);
    elm_var.appendChild(table_div);

    var btn_div_1 = document.createElement("div");
    var btn_div_2 = document.createElement("div");
    var btn_input = document.createElement("input");

    btn_div_1.classList.add("col-sm-12", "col-xl-6");
    btn_div_2.classList.add("bg-light", "rounded", "h-100", "p-1");
    btn_input.classList.add("btn", "btn-outline-primary");

    btn_input.type = "button";
    btn_input.value = "+";
    btn_input.onclick = function() { Add_variable_cat(table_tbody.id); };

    btn_div_1.appendChild(btn_div_2);
    btn_div_2.appendChild(btn_input);
    elm_var.appendChild(btn_div_1);

    elm_var.appendChild(document.createElement("hr"))

    document.getElementById(group_id).appendChild(elm_var);
};

function Del_variable(elm_id, group_id){

    isDel = confirm('Confirm delete variable #' + elm_id.split(".")[2] + "?");

    if(isDel == true){
        var elm_remove = document.getElementById(elm_id);
        elm_remove.remove();
    }

};

function Add_topline_header_item(elm_id){

    var elm = document.getElementById(elm_id);
    var count = elm.children.length;

    lastItemID = elm.children.item(count-1).id;
    arr_lastItemID = lastItemID.split('.');

    newItemID = parseInt(arr_lastItemID[arr_lastItemID.indexOf('row') - 1]) + 1;
    strNewItemID = "detail.topline_design.header." + newItemID.toString();

    tr = document.createElement("tr");
    td_name = document.createElement("td");
    td_lbl = document.createElement("td");
    td_hid = document.createElement("td");
    td_btn = document.createElement("td");

    tr.id = strNewItemID + ".row";

    td_name.width = "40%";
    td_lbl.width = "20%";
    td_hid.width = "35%";
    td_btn.width = "5%";

    ipt_name = document.createElement("input");
    ipt_lbl = document.createElement("input");
    ipt_hid = document.createElement("input");
    ipt_btn = document.createElement("input");

    ipt_name.type = "text"
    ipt_name.classList.add("form-control");
    ipt_name.id = strNewItemID + ".name";
    ipt_name.name = ipt_name.id

    ipt_lbl.type = "text"
    ipt_lbl.classList.add("form-control");
    ipt_lbl.id = strNewItemID + ".lbl";
    ipt_lbl.name = ipt_lbl.id

    ipt_hid.type = "text"
    ipt_hid.classList.add("form-control");
    ipt_hid.id = strNewItemID + ".hidden_cats";
    ipt_hid.name = ipt_hid.id

    ipt_btn.type = "button"
    ipt_btn.classList.add("btn", "btn-outline-danger");
    ipt_btn.id = strNewItemID + ".btn_del";
    ipt_btn.value = "X";
    ipt_btn.setAttribute('onclick', "Del_topline_header_item('" + tr.id + "')");

    tr.appendChild(td_name);
    tr.appendChild(td_lbl);
    tr.appendChild(td_hid);
    tr.appendChild(td_btn);

    td_name.appendChild(ipt_name);
    td_lbl.appendChild(ipt_lbl);
    td_hid.appendChild(ipt_hid);
    td_btn.appendChild(ipt_btn);

    elm.appendChild(tr);

};

function Del_topline_header_item(elm_id){

    isDel = confirm('Confirm delete variable #' + elm_id + "?");

    if(isDel == true){
        var elm = document.getElementById(elm_id);
        elm.remove();
    }
};

function Add_topline_side_item(elm_id) {

    var elm = document.getElementById(elm_id);
    var count = elm.children.length;

    lastItemID = elm.children.item(count-1).id;
    arr_lastItemID = lastItemID.split('.');

    newItemID = parseInt(arr_lastItemID[arr_lastItemID.length - 1]) + 1;
    strNewItemID = "detail.topline_design.side." + newItemID.toString();

    sideItem = document.createElement("div");
    sideItem.classList.add("row", "g-0", "p-2");
    sideItem.id = strNewItemID;

    div1 = document.createElement("div");
    div1.classList.add("d-flex", "align-items-center", "justify-content-between", "p-1");

    div1_h6 = document.createElement("h6");
    div1_h6.classList.add("mb-1");
    div1_h6.innerHTML = "#" + newItemID.toString();

    btn_del_item = document.createElement("input");
    btn_del_item.type = "button"
    btn_del_item.classList.add("btn", "btn-outline-danger");
    btn_del_item.value = "Delete";
    btn_del_item.setAttribute('onclick', "Del_topline_side_item('" + sideItem.id + "')");

    sideItem.appendChild(div1);
    div1.appendChild(div1_h6);
    div1.appendChild(btn_del_item);

    arr = ['group_lbl', 'name', 'lbl', 'type', 't2b|b2b|mean', 'is_count|is_corr|is_ua', 'ma_cats', 'hidden_cats'];
    for(var i = 0; i < arr.length; i++)
    {
        div_sub1 = document.createElement("div");
        div_sub1.classList.add("col-sm-12", "col-xl-6");

        div_sub2 = document.createElement("div");
        div_sub2.classList.add("form-floating", "p-1");

        if (arr[i] == 'group_lbl' || arr[i] == 'name' || arr[i] == 'lbl' || arr[i] == 'ma_cats' || arr[i] == 'hidden_cats') {

            ipt_item = document.createElement("input");
            ipt_item.type = "text";
            ipt_item.classList.add("form-control");
            ipt_item.id = strNewItemID + "." + arr[i];
            ipt_item.name = ipt_item.id;

            label_item = document.createElement("label");
            label_item.htmlFor = ipt_item.id;

            if (arr[i] == 'group_lbl') {
                label_item.innerHTML = "Group";
            }
            else if(arr[i] == 'name') {
                label_item.innerHTML = "Name";
            }
            else if(arr[i] == 'lbl') {
                label_item.innerHTML = "Label";
            }
            else if(arr[i] == 'ma_cats') {
                label_item.innerHTML = "MA Categories";
            }
            else if(arr[i] == 'hidden_cats') {
                label_item.innerHTML = "Hidden categories";
            }


        }
        else if (arr[i] == 'type') {

            ipt_item = document.createElement("select");
            ipt_item.classList.add("form-select");
            ipt_item.id = strNewItemID + "." + arr[i];
            ipt_item.name = ipt_item.id;
            ipt_item.setAttribute('onchange', "topline_side_type(this);");

            arr_sel_item = ['OL', 'JR', 'FC', 'SA', 'MA', 'NUM'];
            for(var j = 0; j < arr_sel_item.length; j++) {
                sel_item = document.createElement("option");
                sel_item.value = arr_sel_item[j];
                sel_item.innerHTML = sel_item.value
                ipt_item.appendChild(sel_item);
            }

            label_item = document.createElement("label");
            label_item.htmlFor = ipt_item.id;
            label_item.innerHTML = "Type";

        }
        else if (arr[i] == 't2b|b2b|mean' || 'is_count|is_corr|is_ua') {

            sub_arr = arr[i].split('|');

            for(var j = 0; j < sub_arr.length; j++) {
                div_sub3 = document.createElement("div");
                div_sub3.classList.add("form-check", "form-check-inline", "form-switch");

                ipt_item = document.createElement("input");
                ipt_item.type = "checkbox";
                ipt_item.classList.add("form-check-input");
                ipt_item.setAttribute('role', "switch");
                ipt_item.id = strNewItemID + "." + sub_arr[j];
                ipt_item.name = ipt_item.id;
                ipt_item.setAttribute('onclick', "cbxClick(this, '" + ipt_item.id + "');");

                label_item = document.createElement("label");
                label_item.htmlFor = ipt_item.id;

                if (sub_arr[j] == 't2b') {
                    label_item.innerHTML = "T2B";
                }
                else if(sub_arr[j] == 'b2b') {
                    label_item.innerHTML = "B2B";
                }
                else if(sub_arr[j] == 'mean') {
                    label_item.innerHTML = "Mean";
                }
                else if(sub_arr[j] == 'is_count') {
                    label_item.innerHTML = "Display count";
                }
                else if(sub_arr[j] == 'is_corr') {
                    label_item.innerHTML = "Correlation";
                }
                else if(sub_arr[j] == 'is_ua') {
                    label_item.innerHTML = "U&A";
                }

                div_sub3.appendChild(ipt_item);
                div_sub3.appendChild(label_item);
                div_sub2.appendChild(div_sub3);
            }

        }

        sideItem.appendChild(div_sub1);
        div_sub1.appendChild(div_sub2);

        if (arr[i] != 't2b|b2b|mean' && arr[i] != 'is_count|is_corr|is_ua') {
            div_sub2.appendChild(ipt_item);
            div_sub2.appendChild(label_item);
        }

    }

    sideItem.appendChild(document.createElement("hr"));

    elm.appendChild(sideItem);

};

function Del_topline_side_item(elm_id, group_id){

    isDel = confirm('Confirm delete variable #' + elm_id.split(".")[3] + "?");

    if(isDel == true){
        var elm_remove = document.getElementById(elm_id);
        elm_remove.remove();
    }
};

function topline_side_type(sel) {
    itemID = (sel.id).replace("type", "");

    elm_t2b = document.getElementById(itemID + "t2b");
    elm_b2b = document.getElementById(itemID + "b2b");
    elm_mean = document.getElementById(itemID + "mean");

    elm_ma_cats = document.getElementById(itemID + "ma_cats");
    elm_hidden_cats = document.getElementById(itemID + "hidden_cats");

    elm_is_count = document.getElementById(itemID + "is_count");
    elm_is_corr = document.getElementById(itemID + "is_corr");
    elm_is_ua = document.getElementById(itemID + "is_ua");

    selVal = sel.value;
    switch(selVal) {
        case 'OL':
            elm_t2b.checked = true;
            elm_b2b.checked = true;
            elm_mean.checked = true;

            elm_is_count.checked = false;
            elm_is_corr.checked = true;
            elm_is_ua.checked = false;

            elm_t2b.value = "true";
            elm_b2b.value = "true";
            elm_mean.value = "true";

            elm_is_count.value = "false";
            elm_is_corr.value = "true";
            elm_is_ua.value = "false";

            elm_ma_cats.value = "";
            elm_hidden_cats.value = "";

            break;

        case 'JR':
            elm_t2b.checked = true;
            elm_b2b.checked = true;
            elm_mean.checked = true;

            elm_is_count.checked = false;
            elm_is_corr.checked = false;
            elm_is_ua.checked = false;

            elm_t2b.value = "true";
            elm_b2b.value = "true";
            elm_mean.value = "true";

            elm_is_count.value = "false";
            elm_is_corr.value = "false";
            elm_is_ua.value = "false";

            elm_ma_cats.value = "";
            elm_hidden_cats.value = "";

            break;

        case 'FC':

            elm_t2b.checked = false;
            elm_b2b.checked = false;
            elm_mean.checked = false;

            elm_is_count.checked = false;
            elm_is_corr.checked = false;
            elm_is_ua.checked = false;

            elm_t2b.value = "false";
            elm_b2b.value = "false";
            elm_mean.value = "false";

            elm_is_count.value = "false";
            elm_is_corr.value = "false";
            elm_is_ua.value = "false";

            elm_ma_cats.value = "";
            elm_hidden_cats.value = "";

            break;

        case 'SA':

            elm_t2b.checked = false;
            elm_b2b.checked = false;
            elm_mean.checked = false;

            elm_is_count.checked = false;
            elm_is_corr.checked = false;
            elm_is_ua.checked = true;

            elm_t2b.value = "false";
            elm_b2b.value = "false";
            elm_mean.value = "false";

            elm_is_count.value = "false";
            elm_is_corr.value = "false";
            elm_is_ua.value = "true";

            elm_ma_cats.value = "";
            elm_hidden_cats.value = "";

            break;

        case 'MA':

            elm_t2b.checked = false;
            elm_b2b.checked = false;
            elm_mean.checked = false;

            elm_is_count.checked = false;
            elm_is_corr.checked = false;
            elm_is_ua.checked = true;

            elm_t2b.value = "false";
            elm_b2b.value = "false";
            elm_mean.value = "false";

            elm_is_count.value = "false";
            elm_is_corr.value = "false";
            elm_is_ua.value = "true";

            break;

        case 'NUM':

            elm_t2b.checked = false;
            elm_b2b.checked = false;
            elm_mean.checked = false;

            elm_is_count.checked = false;
            elm_is_corr.checked = false;
            elm_is_ua.checked = true;

            elm_t2b.value = "false";
            elm_b2b.value = "false";
            elm_mean.value = "false";

            elm_is_count.value = "false";
            elm_is_corr.value = "false";
            elm_is_ua.value = "true";

            elm_ma_cats.value = "";
            elm_hidden_cats.value = "";

            break;

    }

};

function fnc_submit_clear_data(){
    isSubmit = confirm('Confirm clear data?');

    elm = document.getElementById("form_data_clear")

    if (isSubmit == true) {

        elm.addEventListener('submit', (e) => {
            e.preventDefault();
            elm.submit();
        });
    }
    else
    {
        elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
};

function submit_export_data(form_id) {

    form_elm = document.getElementById(form_id);

    selSection = document.getElementById("export_section");

    if(selSection.value == '-1'){
        alert("Please select the export section!");
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
    else {
        isConfirm = confirm('Confirm export data for ' + selSection.options[selSection.selectedIndex].text + '?');

        if(isConfirm == true){

            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
                form_elm.submit();
            });
        }
        else
        {
            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
        }
    }
};

function fnc_process_tl_submit(btn, form_id){

    sel_elm = document.getElementById("export_tl_section");
    form_elm = document.getElementById(form_id);

    if(sel_elm.value == '-1')
    {
        alert("Please select the export section!");
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
    else
    {
        val1 = document.getElementById("export_tl_section_1");

        val1.value = sel_elm.value;

        isConfirm = confirm('Confirm export topline for ' + sel_elm.options[sel_elm.selectedIndex].text + '?');

        if(isConfirm == true) {

            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
                form_elm.submit();
            });

        }
        else
        {
            form_elm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
        }

    }

};

function fnc_tl_submit(btn, form_id, lbl){

    form_elm = document.getElementById(form_id);

    isConfirm = confirm('Confirm export ' + lbl + '?');

    if(isConfirm == true) {

        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
            form_elm.submit();
        });

    }
    else
    {
        form_elm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }

};

//END MSN_PRJ_ID

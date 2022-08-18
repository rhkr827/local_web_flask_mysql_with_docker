
// dataset from python
var jobhistory;
var jobsummary;
// will make dynamic table
function initialize(jh, js) {
    jobhistory = jh;
    jobsummary = js;
    create_dynamic_table(jobhistory);

    return true;
}

function click_tab() {
    if (this.event.target.className == 'li0')
        create_dynamic_table(jobhistory)
    else
        create_dynamic_table(jobsummary)
}

function create_dynamic_table(json_data) {
    var content = document.getElementById('content');
    var exist_tbl = document.getElementById('dynaTbl')
    if (exist_tbl != null) {
        content.removeChild(exist_tbl);
    }

    let tbl = document.createElement("table");
    tbl.setAttribute('id', 'dynaTbl');

    if (Object.keys(json_data[0]).length == 7)
        headers = ["company_name", "position", "role", "location", "start_date", "resignation_date", "remark"]
    else
        headers = ["position", "period"]
    let element = '<thead><tr>';
    for (var col = 0; col < headers.length; col++) {
        element += `<th>${headers[col]}</th>`;
    }

    element += '</tr></thead>';
    tbl.innerHTML = element;

    element = null;
    for (var row = 0; row < json_data.length; row++) {
        for (var col = 0; col < headers.length; col++) {
            if (col == 0 && element == null)
                element = '<body><tr>';
            else
                elsment = '<tr>';

            element += `<td>${json_data[row][headers[col]]}</td>`;
        }
        element += '</tr>';
        tbl.innerHTML += element;
        element = null;
    }

    tbl.innerHTML += '</tbody>';
    content.appendChild(tbl);
}
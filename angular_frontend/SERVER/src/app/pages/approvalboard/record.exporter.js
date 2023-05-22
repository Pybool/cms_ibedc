var rowid ; 
var account_num;

function closeModal(id){
    var modal = document.getElementById(id)
    modal.classList.remove('show')
    modal.style.display = 'none'
    modal.setAttribute('aria-hidden',true)
}

function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
}

function exportXlsxData(data,filename)
    {   
        filename = filename + '.xlsx'
        data=[data]
        var ws = window.XLSX.utils.json_to_sheet(data);
        var wb = window.XLSX.utils.book_new();
        window.XLSX.utils.book_append_sheet(wb, ws, "Customer");
        window.XLSX.writeFile(wb,filename);
     }

function exportCSVFile(headers, items, fileTitle) {
    if (headers) {
        items.unshift(headers);
    }

    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);

    var csv = convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

export function exportSingle(type,data,filename){
    
    if(data.length > 0){
        let dataClone = JSON.parse(JSON.stringify(data[0]))
        for(let key of Object.keys(dataClone)){
            dataClone[key] = key.replace(/,/g, '')
        }
        var headers = dataClone;
        var itemsNotFormatted = [data[0]];

        var itemsFormatted = [data[0]];
        var fileTitle = filename; // or 'my-unique-title'
        if (type=='csv'){
            exportCSVFile(headers, itemsFormatted, fileTitle); // call the exportCSVFile() function to process the JSON and trigger the download
            closeModal('exportModal')
        }
        else{
            exportXlsxData(data[0],filename)
            closeModal('exportModal')
        }
        return 
    }
    return alert("Export failed as no data was found for this customer!")

}

export function download(id,account_no){
    rowid = id;
    account_num = account_no
    const modal = document.getElementById('exportModal')
    modal.classList.add('show')
    modal.setAttribute('style', 'display:block !important');
}
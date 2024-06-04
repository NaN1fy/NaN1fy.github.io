function formatSize(size) {
    const KB = 1024;
    const MB = KB * KB;
    const GB = MB * KB;

    if (size >= GB) {
        return `${Math.round(size / GB)} GB`;
    } else if (size >= MB) {
        return `${Math.round(size / MB)} MB`;
    } else if (size >= KB) {
        return `${Math.round(size / KB)} KB`;
    } else {
        return `${size} bytes`;
    }
}

function convertFileName(fileName) {
  
    const patternVE = /^VE_(\d{4})_(\d{2})_(\d{2})(?:_(.*))?$/; // VE_XXX_XX_XX_YY o VE_XXX_XX_XX
    const patternVI = /^VI_(\d{4})_(\d{2})_(\d{2})(?:_(.*))?$/; // VI_XXX_XX_XX o VI_XXX_XX_XX_YY

    if (patternVE.test(fileName)) {
        return fileName.replace(patternVE, function(match, year, month, day, additional) {
            if (additional) {
                return `Verbale esterno del ${year}-${month}-${day} ${additional}`;
            } else {
                return `Verbale esterno del ${year}-${month}-${day} ${additional}`;
            }
        });
    }

    if (patternVI.test(fileName)) {
        return fileName.replace(patternVI, 'Verbale interno del $1-$2-$3');
    }
	return fileName.replace(/_/g, ' ').replace(/\b\w/g, function(char) {
        return char.toUpperCase();
    });
}


function generateHtmlList(data, excludeList, basePath = '') {
    let html = '<ul class="directory-tree">\n';
    for (let item of data) {
        const itemName = item.name;
        const itemPath = basePath + (basePath.endsWith('/') ? '' : '/') + (itemName === 'documents' ? '' : itemName);
        if (item.type === "directory" && !excludeList.includes(itemName)) {
            html += `<li class="folder">${itemName}/</li>\n`;
            html += generateHtmlList(item.contents, excludeList, itemPath);
        } else if (item.type === "file" && !excludeList.includes(itemName)) {
            let fileName = itemName.replace(/(_v\d+\.\d+\.\d+)?\.pdf$/, '');
            fileName = convertFileName(fileName);
            const versionMatch = itemName.match(/_v(\d+\.\d+\.\d+)\.pdf$/); 
            const version = versionMatch ? ` [v${versionMatch[1]}]` : '';
            const fileSize = formatSize(item.size);
            const fileUrl = `https://nan1fy.github.io/docs${itemPath}`;
            html += `<li class="file">${fileName}${version} <a href="${fileUrl}" download>download pdf (${fileSize})</a></li>\n`;
        }
    }
    html += "</ul>\n";
    return html;
}

function appendHtmlToMain(htmlContent) {
	let nuovoElemento = document.createElement('div');
    	nuovoElemento.classList.add('section');
	nuovoElemento.innerHTML = htmlContent;
	let main = document.querySelector('main');
    	main.insertBefore(nuovoElemento, main.lastElementChild);
}

function convertToUTC(dateString) {
    const utcString = dateString.substring(0, 16).replace(' ', 'T');
    return new Date(utcString).toUTCString();
}

function getOffsetForTimezone() {
    return new Date().getTimezoneOffset() * 60 * 1000;
}

let data; 

Promise.all([
    fetch('assets/data/lmod.txt').then(response => response.text()),
    fetch('assets/data/repo_tree.json').then(response => response.json())
])
.then(([data, jsonData]) => {
    const excludeList = [];
    const documentsData = jsonData[0].contents.find(item => item.name === "documents").contents;
    let htmlList = "<h2>Documenti del gruppo</h2>";
    let inputDate = new Date(convertToUTC(data));
    inputDate.setTime(inputDate.getTime() - getOffsetForTimezone())
    console.log(inputDate);
	inputDate.setHours(inputDate.getHours());
	htmlList += generateHtmlList(documentsData, excludeList);
	htmlList += `<span id="dataAgg">Ultimo aggiornamento il ${inputDate.getFullYear()}-${(inputDate.getMonth() + 1).toString().padStart(2, '0')}-${inputDate.getDate().toString().padStart(2, '0')} alle ore ${inputDate.getHours().toString().padStart(2, '0')}:${inputDate.getMinutes().toString().padStart(2, '0')}</span>`;
	appendHtmlToMain(htmlList, "section");
})
.catch(error => console.error('Si è verificato un errore:', error));


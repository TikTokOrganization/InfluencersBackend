/* Template: Tivo - SaaS App HTML Landing Page Template
   Author: Inovatik
   Created: Sep 2019
   Description: Custom JS file
*/

let content;
let categories;
let contentTotal;
let categoryData;
let activeCategory = -1;

let clearImageGrid = function() {
    let imageGrid = document.getElementById("ImageGrid");
    imageGrid.replaceChildren();
};

let initializeImageGrid = function() {
    let rowCounter = 1;
    let row = document.createElement("tr");
    let table = document.getElementById("ImageGrid");
    for(var category = 0; category < categories.length; category++) {
        contentOfCategory = content[categories[category]];
        for(var cont = 0; cont < contentOfCategory.length; cont++) {
            let dataCell = document.createElement("td");
            let link = document.createElement("a");
            let image = document.createElement("img");

            image.setAttribute("src", contentOfCategory[cont]["thumbnailURL"]);
            link.setAttribute("target", "_blank");
            link.setAttribute("href", "https://www.youtube.com/watch?v=" + contentOfCategory[cont]["id"]);

            link.appendChild(image);
            dataCell.appendChild(link);
            row.appendChild(dataCell);

            if(rowCounter % 4 == 0) {
                table.appendChild(row);
                row = document.createElement("tr");
            }
            rowCounter++;
        }
    }
    if(rowCounter % 4 != 0)
        table.appendChild(row);
}

let selectCategory = function() {
    clearImageGrid();

    let selectedCategory = this.id.substring(9, this.id.length);
    if(selectedCategory == activeCategory) {
        activeCategory = -1;
        this.childNodes[0].childNodes[0].style.color = "#333"
        initializeImageGrid();
        return;
    }
    
    let contentOfCategory = content[selectedCategory];
    let numRows = Math.ceil(contentOfCategory.length / 4);

    let counter = 0;
    let table = document.getElementById("ImageGrid");
    for(var i = 0; i < numRows; i++) {
        let row = document.createElement("tr");
        for(var j = 0; j < 4; j++) {
            if(counter < contentOfCategory.length) {
                let dataCell = document.createElement("td");
                let link = document.createElement("a");
                let image = document.createElement("img");

                image.setAttribute("src", contentOfCategory[counter]["thumbnailURL"]);
                link.setAttribute("target", "_blank");
                link.setAttribute("href", "https://www.youtube.com/watch?v=" + contentOfCategory[counter]["id"]);

                link.appendChild(image);
                dataCell.appendChild(link);
                row.appendChild(dataCell);

                counter++;
            }
        }
        table.appendChild(row);
    }

    this.childNodes[0].childNodes[0].style.color = "#bb042b";
    if(activeCategory != -1)
        document.getElementById("Category-" + activeCategory).childNodes[0].childNodes[0].style.color = "#333";

    activeCategory = selectedCategory;
};

let initializeCategoryList = function() {
    let table = document.getElementById("CategorySelector");
    for(var category = 0; category < categories.length; category++) {
        let row = document.createElement("tr");
        let dataCell = document.createElement("td");
        let header6 = document.createElement("h6");
        let text = document.createTextNode(categoryData[categories[category]]);

        header6.appendChild(text);
        dataCell.appendChild(header6);
        row.appendChild(dataCell);
        row.onclick = selectCategory;
        row.setAttribute("id", "Category-" + categories[category]);

        table.appendChild(row);
    }
};


let logOut = function() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost:8080/logOut", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function() {
        if(xhr.response == 200)
            console.log("Successfull log out.");
        else
            console.log("Error logging out.");
    }
    xhr.send();
};

(function($) {
    "use strict"; 
	
    $(window).on("load", function() {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', "http://localhost:8080/getData", true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            let rawData = JSON.parse(xhr.responseText);
            content = rawData["shorts"];
            contentTotal = rawData["total"];
            categoryData = rawData["category_codes"];
            categories = Object.keys(content);
            
            console.log("Total shorts: " + contentTotal);

            initializeCategoryList();
            initializeImageGrid();
        };
        console.log("Before request.");
        xhr.send("refresh=0");
    })
	
})(jQuery);
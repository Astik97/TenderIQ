// ==========================================
// Dashboard JavaScript
// ==========================================

// ==========================================
// Upload Form
// ==========================================

const uploadForm = document.getElementById("uploadForm");

const uploadButton = document.getElementById("uploadButton");

const tenderFiles = document.getElementById("tenderFiles");

const selectedFiles = document.getElementById("selectedFiles");

// ==========================================
// Compare Form
// ==========================================

const compareForm = document.getElementById("compareForm");

// ==========================================
// Show Selected Files
// ==========================================

if(tenderFiles){

    tenderFiles.addEventListener("change",function(){

        if(this.files.length===0){

            selectedFiles.innerHTML="";

            return;

        }

        let html="<strong>Selected Files</strong><br><br>";

        for(let file of this.files){

            html+="📄 "+file.name+"<br>";

        }

        selectedFiles.innerHTML=html;

    });

}

// ==========================================
// Upload Validation
// ==========================================

if(uploadForm){

uploadForm.addEventListener("submit",function(e){

    if(tenderFiles.files.length===0){

        e.preventDefault();

        alert("Please select at least one file.");

        return;

    }

    uploadButton.disabled=true;

    uploadButton.innerText="Uploading...";

});

}

// ==========================================
// Compare Validation
// ==========================================

if(compareForm){

compareForm.addEventListener("submit",function(e){

    const checked=document.querySelectorAll(
        'input[name="selected_tenders"]:checked'
    );

    if(checked.length!==2){

        e.preventDefault();

        alert("Please select exactly TWO tenders.");

    }

});

}

// ==========================================
// Delete Confirmation
// ==========================================

const deleteButtons=document.querySelectorAll(".delete-link");

deleteButtons.forEach(function(button){

button.addEventListener("click",function(e){

const answer=confirm(
"Do you really want to delete this tender?"
);

if(!answer){

e.preventDefault();

}

});

});
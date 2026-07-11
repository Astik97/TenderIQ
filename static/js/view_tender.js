const textArea=document.getElementById("tenderText");

const copyBtn=document.getElementById("copyBtn");

const downloadBtn=document.getElementById("downloadBtn");

const toast=document.getElementById("toast");

copyBtn.onclick=function(){

navigator.clipboard.writeText(textArea.value);

toast.classList.add("show");

setTimeout(()=>{

toast.classList.remove("show");

},2000);

}

downloadBtn.onclick=function(){

const blob=new Blob([textArea.value],{type:"text/plain"});

const link=document.createElement("a");

link.href=URL.createObjectURL(blob);

link.download="Extracted_Tender.txt";

link.click();

}

const text=textArea.value;

document.getElementById("charCount").innerHTML=

"Characters : "+text.length;

document.getElementById("wordCount").innerHTML=

"Words : "+text.trim().split(/\s+/).length;
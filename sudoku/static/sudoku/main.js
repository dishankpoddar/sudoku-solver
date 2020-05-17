image_input = document.getElementById("id_sudoku_image");
if(image_input){
  image_input.oninput = function(){homeButton();}
}
function checkDefault(name) {
  element = document.getElementsByName(name)[0];
  if (element.value != element.defaultValue) element.classList.remove("preset");
  else element.classList.add("preset");
}
function removePicture(){
  document.getElementById("id_sudoku_image").value="";
  homeButton();
}
function homeButton() {
  button = document.getElementById("home_button");
  photo = document.getElementById("id_sudoku_image");
  closeb = document.getElementById("close_button");
  text = document.getElementById("dnd_text");
  if (photo.value != photo.defaultValue) {button.value = "Upload Image";closeb.style = "display:block";text.innerHTML = photo.value.split("\\")[2];}
  else {button.value = "Manual Sudoku";closeb.style = "display:none";text.innerHTML = "Drag your image or click here.";}
}
function resetSudoku(){
  document.getElementById('sudoku_form').reset();
  let inboxes = document.getElementsByClassName("inbox");
  for (i = 0; i < inboxes.length; i++) {
    if (inboxes[i].defaultValue != 0) inboxes[i].classList.add("preset");
  }
}
function clearSudoku() {
  //document.getElementById('sudoku_form').reset();
  let inboxes = document.getElementsByClassName("inbox");
  for (i = 0; i < inboxes.length; i++) {
    inboxes[i].value = "";
    inboxes[i].classList.remove("preset");
  }
}
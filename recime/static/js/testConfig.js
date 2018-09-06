//Adds mutliple ingredients
function addEntry() {
  //Val is the pam tuning param we are adding
  var val = document.getElementById("itemsInput").value;
  //Container should have the italic description and the button in it
  var container = document.getElementById("container");
  //This puts the input for editing in the container, but makes it invisible until the expand button is pressed
  var input = document.createElement("input");
  //The descritpion that is added to the container. Shows what previously was added
  var descr = document.createElement("em");
  //This is the id for the italic placeholder essentially
  var paragraph = document.getElementById("description");
  //The span and button are the combinations bootstrap needs to create a glyph icon button
  var span = document.createElement("span");
  var button = document.createElement("p");

  input.type = "text";
  input.value = val;
  input.name = "items";
  input.id = "tuneID";
  input.className = "form-control"
  input.style = "display:none;"
  container.appendChild(input);

  descr.innerHTML = val + " added."
  descr.style = "display:inline;"

  span.onclick = function() {
    expand()
  }
  button.style = "cursor:pointer; display:inline"
  span.className = "glyphicon glyphicon-collapse-down"
  button.appendChild(span);
  //First remove the last thing in the paragraph so we can add the new description
  while (paragraph.firstChild) {
    paragraph.removeChild(paragraph.firstChild);
  }
  paragraph.appendChild(descr);
  paragraph.appendChild(button);

  document.getElementById("itemsInput").value = "";
}
//Reduce the view so that all the entries are not showing anymore
function reduce() {
  //Container is what will hold the editable rows, paragraph we just want to delete all together
  var container = document.getElementById("container");
  var paragraph = document.getElementById("description");
  //The span and button are the combinations bootstrap needs to create a glyph icon button
  //Also we want to just add the last element description
  var span = document.createElement("span");
  var button = document.createElement("p");
  var descr = document.createElement("em");

  //Get all the tuning parameters first, then delete everything in the container, so we can
  //Add them back, but this time not invisible haha
  names = document.getElementsByName("items");
  //First clean out any accidental entries like spaces or empty button presses
  var array = []
  for (i=0; i <= (names.length); i++) {
    if (names[i] != undefined && names[i].value != "") {
      array.push(names[i].value)
    }
  }
  while (container.firstChild) {
    container.removeChild(container.firstChild)
  }
  //Now we add the text fields back in
  for (i=0; i < array.length; i++) {
    var input = document.createElement("input");
    input.type = "text";
    input.value = array[i];
    input.name = "items";
    input.className = "form-control"
    input.style = "display:none;"
    container.appendChild(input);
  }
  span.onclick = function() {
    expand()
  }
  button.style = "cursor:pointer; display:inline"
  span.className = "glyphicon glyphicon-collapse-down"
  button.appendChild(span);
  descr.innerHTML = array[array.length - 1] + " added."
  descr.style = "display:inline;"
  //First remove the last thing in the paragraph so we can add the new description
  while (paragraph.firstChild) {
    paragraph.removeChild(paragraph.firstChild);
  }
  paragraph.appendChild(descr);
  paragraph.appendChild(button);
}
//Expand the elements so that you can edit any params you wrote
function expand() {
  //Container is what will hold the editable rows, paragraph we just want to delete all together
  var container = document.getElementById("container");
  var paragraph = document.getElementById("description");
  //The span and button are the combinations bootstrap needs to create a glyph icon button
  var span = document.createElement("span");
  var button = document.createElement("p");
  span.onclick = function() {
    reduce()
  }
  button.style = "cursor:pointer; display:inline"
  span.className = "glyphicon glyphicon-collapse-up"
  button.appendChild(span);

  while (paragraph.firstChild) {
    paragraph.removeChild(paragraph.firstChild);
  }
  //Get all the tuning parameters first, then delete everything in the container, so we can
  //Add them back, but this time not invisible haha
  names = document.getElementsByName("items");
  //First clean out any accidental entries like spaces or empty button presses
  var array = []
  for (i=0; i <= (names.length); i++) {
    if (names[i] != undefined && names[i].value != "") {
      array.push(names[i].value)
    }
  }
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  //Now we add the text fields back in
  for (i=0; i < array.length; i++) {
    var input = document.createElement("input");
    input.type = "text";
    input.value = array[i];
    input.name = "items";
    input.className = "form-control"
    container.appendChild(document.createElement("br"))
    container.appendChild(input);
  }
  container.appendChild(button)
}

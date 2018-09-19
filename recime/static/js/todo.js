function check(id) {
  var boxID = "box" + id;
  var vals = document.getElementsByName(id).forEach(function(ele) {
    if (document.getElementById(boxID).checked) {
      $(ele).css("text-decoration", "line-through");
    } else {
      $(ele).css("text-decoration", "none");
    }
  });
}

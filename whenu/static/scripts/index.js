function search(e) {
  if (e.keyCode == 13) {
    if($("#query").val() != "" && $("#query").val() != undefined) {
      if(window.location.href.lastIndexOf('/') + 1 == window.location.href.length)
      window.location.replace(window.location.href + "search/?food=" + $("#query").val());
      else
      window.location.replace(window.location.href + "/search/?food=" + $("#query").val());
    }
  }
}

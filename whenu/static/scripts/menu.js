function search(e) {
  if (e.keyCode == 13) {
    if($("#query").val() != "" && $("#query").val() != undefined) {
      console.log(window.location.href);
      window.location.replace(window.location.href.substring(0, window.location.href.indexOf("=") + 1) + $("#query").val());
    }
  }
}

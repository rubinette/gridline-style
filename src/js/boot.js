(function () {
  var r = document.documentElement;
  r.className = r.className.replace(/\bno-js\b/, "js");
  try {
    var t = localStorage.getItem("gridline-theme");
    if (t === "light" || t === "dark") r.setAttribute("data-theme", t);
  } catch (e) {}
})();

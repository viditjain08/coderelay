$(document).ready(function(){
  if("{{code.code|escapejs}}"!="") {

  sourceEditor.setValue("{{code.code|escapejs}}");
  document.getElementById("selectLanguageBtn").value={{code.lang}};

};

var timex = Math.floor({{time}}-120-Date.parse(new Date())/1000);
var timey = Math.floor({{time}}-Date.parse(new Date())/1000);
console.log(timex);
setTimeout(x, timex*1000);
setTimeout(y, timey*1000);
function y() {
    document.getElementById("saveBtn").click();

    $.ajax({
        url: '/ajax/swapcode/',
        data: {
          'code': sourceEditor.getValue(),
          'lang': $("#selectLanguageBtn").val(),
        },
        dataType: 'json',
        success: function (data) {
            if(data.finish) {
              document.getElementById("finishRace").click();
            }
            //outputEditor.setValue(data.output);
            document.getElementById("q").innerHTML = data.question;
            sourceEditor.setValue(data.code);
            $("#timer").hide();
            document.getElementById("selectLanguageBtn").value=data.lang;
            var timex1 = Math.floor(data.time-120-Date.parse(new Date())/1000);

            var timey1 = Math.floor(data.time - Date.parse(new Date())/1000);
            setTimeout(x, timex1*1000);

            setTimeout(y, timey1*1000);

          
        }
      });}
function x() {
var myVar = setInterval(myTimer, 1000);
function myTimer() {
    document.getElementById("timer").innerHTML = {{time}}-Date.parse(new Date())/1000;
};
};

  $("#runBtn").click(function(e) {
    $.ajax({
        url: '/ajax/runcode/',
        data: {
          'code': sourceEditor.getValue(),
          'input': inputEditor.getValue(),
          'lang': $("#selectLanguageBtn").val(),
        },
        dataType: 'json',
        success: function (data) {
            if(data.finish) {
              document.getElementById("finishRace").click();
            }
            console.log(data.output);

            //outputEditor.setValue(data.output);
            document.getElementById("abc").innerHTML = data.output;
          
        }
      });
  });

  });


document.onkeydown = function (e) {
  var key = e.charCode || e.keyCode;
  if (key == 123 || key == 122 || e.ctrlKey) { 
    // enter key do nothing
    e.preventDefault();
  }

     
}



$(document).ready(function(){
document.addEventListener('contextmenu', event => event.preventDefault());
  $("#saveBtn").click(function(e) {
    $.ajax({
        url: '/ajax/savecode/',
        data: {
          'code': sourceEditor.getValue(),
          'lang': $("#selectLanguageBtn").val(),
          'question': '{{qid}}',
        },
        dataType: 'json',
        success: function (data) {
            if(data.finish) {
              document.getElementById("finishRace").click();
            }
            console.log(data);

        }
      });


  });

  $("#submitBtn").click(function(e) {
    $.ajax({
        url: '/ajax/submitques/',
        data: {
          'code': sourceEditor.getValue(),
          'lang': $("#selectLanguageBtn").val(),
          'question': '{{qid}}',
        },
        dataType: 'json',
        success: function (data) {
            if(data.finish) {
              document.getElementById("finishRace").click();
            }
            insertTemplate();
            if(!data.done) {
            document.getElementById("q").innerHTML = data.question;
          }

        }
      });


  });


    $("#finishRace").click(function(e) {
    $.ajax({
        url: '/ajax/finishrace/',
        data: {
          'code': sourceEditor.getValue(),
          'lang': $("#selectLanguageBtn").val(),
        },
        dataType: 'json',
        success: function (data) {
            window.location = "/logout";

        }
      });


  });



  });

var flag=0;
if (document.addEventListener)
{
    document.addEventListener('webkitfullscreenchange', exitHandler, false);
    document.addEventListener('mozfullscreenchange', exitHandler, false);
    document.addEventListener('fullscreenchange', exitHandler, false);
    document.addEventListener('MSFullscreenChange', exitHandler, false);
}

function exitHandler()
{
    if (document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement !== null)
    {
        console.log(flag);
        if(flag==1) {
        	window.location = "/logout";
        }
        flag=1;

    }
}


 window.addEventListener('blur', stopTimer);
 
  function stopTimer() {
  window.location = "/logout";
 }

// Find the right method, call on correct element
function launchFullscreen(element) {
  if(element.requestFullscreen) {
    element.requestFullscreen();
  } else if(element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if(element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen();
  } else if(element.msRequestFullscreen) {
    element.msRequestFullscreen();
  }

}

function exitFullscreen() {
  if(document.exitFullscreen) {
    document.exitFullscreen();
  } else if(document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if(document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  }
}

function dumpFullscreen() {
  console.log("document.fullscreenElement is: ", document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement);
  console.log("document.fullscreenEnabled is: ", document.fullscreenEnabled || document.mozFullScreenEnabled || document.webkitFullscreenEnabled || document.msFullscreenEnabled);

}

// Events
document.addEventListener("fullscreenchange", function(e) {
  console.log("fullscreenchange event! ", e);
});
document.addEventListener("mozfullscreenchange", function(e) {
  console.log("mozfullscreenchange event! ", e);
});
document.addEventListener("webkitfullscreenchange", function(e) {
  console.log("webkitfullscreenchange event! ", e);
});
document.addEventListener("msfullscreenchange", function(e) {
  console.log("msfullscreenchange event! ", e);
});

// Add different events for fullscreen

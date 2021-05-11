


function style_decode(){
  var x = document.getElementById('encode');
  var y = document.getElementById('decode');
  var z = document.getElementById('btn');
  x.style.left = "-530px";
  y.style.left = "220px";
  z.style.left = "110px";
}

function style_encode(){
  var x = document.getElementById('encode');
  var y = document.getElementById('decode');
  var z = document.getElementById('btn');
  x.style.left = "220px";
  y.style.left = "750px";
  z.style.left = "0px";
}





async function js_encode() {

 var img = document.getElementById("enc-img").files[0].name;
 var file_to_read = document.getElementById("enc-file_to_read").files[0].name;
 var new_img_name = document.getElementById("enc-new_img_name").value;
 var x = await eel.hide(img, file_to_read, new_img_name)();
 if (x == "success"){
  alert("Message successfully hidden inside image file! Please check your directory :)");
 }
 else{
  alert("Oops..Something went wrong. Please fill in the fields correctly :)");
 }

}
async function js_decode() {
  var img = document.getElementById("dec-img").files[0].name;
  var new_file_name = document.getElementById("dec-new_file_name").value;
  var x = await eel.extract(img, new_file_name)();
  if (x == "success"){
   alert("Message successfully extracted into text file! Please check your directory :)");
  }
  else{
   alert("Oops..Something went wrong. Please fill in the fields correctly :)");
  }
}





async function jss_encode() {
 var sound_path = document.getElementById("enc-sound_path").files[0].name;
 var file_path = document.getElementById("enc-file_path").files[0].name;
 var output_path = document.getElementById("enc-output_path").value;
 var num_lsb = parseInt(document.getElementById("enc-num_lsb").value);


 var x = await eel.hide_data(sound_path, file_path, output_path, num_lsb)();
 if (x == "success"){
  alert("Message successfully hidden inside audio file! Please check your directory :)");
 }
 else{
  alert("Oops..Something went wrong. Please fill in the fields correctly :)");
 }
}
async function jss_decode() {
  var sound_path = document.getElementById("dec-sound_path").files[0].name;
  var file_path = document.getElementById("dec-file_path").value;
  var num_lsb = parseInt(document.getElementById("dec-num_lsb").value);
  var bytes_to_recover = parseInt(document.getElementById("dec-bytes_to_recover").value);

  var x = await eel.extract_data(sound_path, file_path, num_lsb, bytes_to_recover)();
  if (x == "success"){
   alert("Message successfully extracted into text file! Please check your directory :)");
  }
  else{
   alert("Oops..Something went wrong. Please fill in the fields correctly :)");
  }

}

const eye_icon = document.getElementById("eye-icon");
const pronunciation = document.getElementById("pronunciation");
const sound_speaker_icon = document.getElementById("sound-speaker-icon");
const translation = document.getElementById("translation");
const word = document.getElementById("word");
const phonetics = document.getElementById("phonetics");
const remember_word = document.getElementById("remember-word");
const dont_remember_word = document.getElementById("dont-remember-word");

eye_icon.addEventListener("click", show_translation);
sound_speaker_icon.addEventListener("click", play_audio);
remember_word.addEventListener("click", user_remember_word);
dont_remember_word.addEventListener("click", user_dont_remember_word);

let data;

get_data();

// get data from views.py via AJAX
function get_data(){
  $.ajax({
      url: "/repeat/",
      type: "GET",
      dataType: "json",
      success: (words) => {
        data = words["repeat_words"];
        console.log(data); 
        main();
      },
      error: (error) => {
        console.log(error);
      }
    });
}

// send data to views.py via AJAX
function send_data(word_status_info){
  $.ajax({
    url: "/repeat/",
    method : "post",
    dataType : "json",
    data : {main: JSON.stringify(word_status_info), "csrfmiddlewaretoken": document.getElementsByName("csrfmiddlewaretoken")[0].value},
    });
}

function main(){
  hide_translation();
  if (data.length != 0){
    add_info_to_card(data[0]);
  }
  else{
    word.innerHTML = "Поки слів для повторення немає";
    sound_speaker_icon.style.display = "none";
    phonetics.style.display = "none";
    eye_icon.style.display = "none";
    remember_word.style.display = "none";
    dont_remember_word.style.display = "none";
  }
}

function add_info_to_card(word_info){
  word.innerHTML = word_info["translation"];
  phonetics.innerHTML = word_info["phonetics"];
  pronunciation.src = word_info["audio_link"];
  translation.innerHTML = word_info["word"];
}

function user_remember_word(){
  send_data({"word_id": data[0]["id"]});
  data.splice(0, 1);
  main();
}

function user_dont_remember_word(){
  data.splice(0, 1);
  main();
}

function show_translation(){
    eye_icon.style.display = "none";
    translation.style.display = "flex";
    phonetics.style.display = "flex";
    sound_speaker_icon.style.display = "flex";
}

function hide_translation(){
  eye_icon.style.display = "flex";
  translation.style.display = "none";
  phonetics.style.display = "none";
  sound_speaker_icon.style.display = "none";
}

function play_audio(){
    pronunciation.play();
}
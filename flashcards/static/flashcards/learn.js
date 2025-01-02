const eye_icon = document.getElementById("eye-icon");
const pronunciation = document.getElementById("pronunciation");
const sound_speaker_icon = document.getElementById("sound-speaker-icon");
const translation = document.getElementById("translation");
const word = document.getElementById("word");
const phonetics = document.getElementById("phonetics");
const skip_word = document.getElementById("skip-word");
const learn_word = document.getElementById("learn-word");

eye_icon.addEventListener("click", show_translation);
sound_speaker_icon.addEventListener("click", play_audio);
skip_word.addEventListener("click", show_next_word)
learn_word.addEventListener("click", show_next_word)

let data;
get_data();


// get data from views.py via AJAX
function get_data(){
  $.ajax({
      url: "/learn/",
      type: "GET",
      dataType: "json",
      success: (english_words) => {
        data = english_words["english_words"];
        console.log(data);
        add_info();
      },
      error: (error) => {
        console.log(error);
      }
    });
}

// add information to card
function add_info(){ 
  console.log(data[0]);
  word.innerHTML = data[0]["word"];
  phonetics.innerHTML = data[0]["phonetics"];
  pronunciation.src = data[0]["audio_link"];
  translation.innerHTML = data[0]["translation"];
}

function show_next_word(){
  hide_translation();
  data.splice(0, 1);
  add_info();
}

function show_translation(){
    eye_icon.style.display = "none";
    translation.style.display = "flex";
}

function hide_translation(){
  eye_icon.style.display = "flex";
  translation.style.display = "none";
}

function play_audio(){
    pronunciation.play();
}
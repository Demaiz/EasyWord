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

let selected_words;
let learning_words;

get_data();

// get data from views.py via AJAX
function get_data(){
  $.ajax({
      url: "/learn/",
      type: "GET",
      dataType: "json",
      success: (words) => {
        selected_words = words["selected_words"];
        learning_words = words["learning_words"];        
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
    url: "/learn/",
    method : "post",
    dataType : "json",
    data : {main: JSON.stringify(word_status_info), "csrfmiddlewaretoken": document.getElementsByName("csrfmiddlewaretoken")[0].value},
    });
}

function main(){
  hide_translation();
  if(learning_words.length != 0){
    // сhange button values and add/remove event listeners if needed
    learn_word.value = "Запам'ятав це слово";
    skip_word.value = "Не пам'ятаю це слово";

    learn_word.removeEventListener("click", user_want_to_learn_word);
    skip_word.removeEventListener("click", user_already_know_word);

    learn_word.addEventListener("click", user_memorized_word);
    skip_word.addEventListener("click", user_forgot_word);
    add_info_to_card(learning_words[0]);
  }

  else if(selected_words.length != 0){
    // сhange button values and add/remove event listeners if needed
    learn_word.value = "Вчити це слово";
    skip_word.value = "Я вже знаю це слово";

    learn_word.removeEventListener("click", user_memorized_word);
    skip_word.removeEventListener("click", user_forgot_word);

    learn_word.addEventListener("click", user_want_to_learn_word);
    skip_word.addEventListener("click", user_already_know_word);
    add_info_to_card(selected_words[0]);
  }

  else{ // if both arrays are empty, get data from server
    get_data();
  }

}

function add_info_to_card(word_info){
  word.innerHTML = word_info["word"];
  phonetics.innerHTML = word_info["phonetics"];
  pronunciation.src = word_info["audio_link"];
  translation.innerHTML = word_info["translation"];
}

function user_forgot_word(){
  learning_words.splice(0, 1); // remove current word from array
  main();
}

function user_already_know_word(){
  send_data({"status": "known", "word_id": selected_words[0]["id"]}); // update word status
  selected_words.splice(0, 1); // remove current word from array
  main();
}

function user_want_to_learn_word(){
  send_data({"status": "learning", "word_id": selected_words[0]["id"]}); // update word status
  selected_words.splice(0, 1); // remove current word from array
  main();
}

function user_memorized_word(){
  send_data({"status": "repeating", "word_id": learning_words[0]["id"]}); // update word status
  learning_words.splice(0, 1); // remove current word from array
  main();
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
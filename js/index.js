const g = document.querySelector('g');
const circle = document.querySelector('circle');
const smile = document.querySelector('.smile');

const input = document.querySelector('.checker__input');
const label = document.querySelector('.checker');
const text = document.querySelector('.checker__text');

function changeSmile() {
    if (input.checked === true) {
        text.textContent = 'I look happy, am I?';
        smile.style = 'transform: scale(1, 1); transform-origin: 46% 70%;';
    } else {
        text.textContent = 'I have seen some kind of s...';
        smile.style = 'transform: scale(1, -1); transform-origin: 46% 70%;';
    }
}

label.addEventListener('click', changeSmile);
changeSmile();

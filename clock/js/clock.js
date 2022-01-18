// Реализация анимации часов

let hands = [];
hands.push(document.querySelector('.clock__second > *'));
hands.push(document.querySelector('.clock__minute > *'));
hands.push(document.querySelector('.clock__hour > *'));

const cx = 100;
const cy = 100;

function shifter(val) {
    return [val, cx, cy].join(' ');
}


const date = new Date();
const hoursAngle = 360 * date.getHours() / 12 + date.getMinutes() / 2;
const minuteAngle = 360 * date.getMinutes() / 60;
const secAngle = 360 * date.getSeconds() / 60;

function setShifter(element, shifterParam) {
    element.setAttribute('from', shifter(shifterParam))
    element.setAttribute('to', shifter(shifterParam + 360))
}

setShifter(hands[0], secAngle)
setShifter(hands[1], minuteAngle)
setShifter(hands[2], hoursAngle)


for(let i = 1; i <= 12; i++) {
    let el = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    el.setAttribute('x1', '100');
    el.setAttribute('y1', '30');
    el.setAttribute('x2', '100');
    el.setAttribute('y2', '40');
    el.setAttribute('transform', 'rotate(' + (i*360/12) + ' 100 100)');
    el.setAttribute('class', 'clock__indicator');
    document.querySelector('.clock').appendChild(el);
}

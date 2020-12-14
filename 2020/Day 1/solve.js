const fs = require("fs");

const file = fs.readFileSync("./data.txt", "utf8");
const rawValues = file.split("\r\n").map((str) => parseInt(str));

const getPart1 = (index = 0) => {
  const current = rawValues[index];
  for (let i = index + 1; i < rawValues.length; ++i) {
    if (current + rawValues[i] === 2020) {
      console.log("result", current * rawValues[i]);
      break;
    }
  }
  ++index;
  if (index < rawValues.length) getPart1(index);
};

getPart1();

const getPart2 = (index1 = 0, index2 = 0) => {
  const current = rawValues[index1];
  const next = rawValues[index2];
  for (let i = 0; i < rawValues.length; ++i) {
    if (i === index1 || i === index2) continue;
    if (current + next + rawValues[i] === 2020) {
      console.log("result", current * next * rawValues[i]);
      break;
    }
  }
  ++index1;
  if (index1 >= rawValues.length) {
    index1 = 0;
    index2++;
  }
  if (index2 < rawValues.length) getPart2(index1, index2);
};

getPart2();

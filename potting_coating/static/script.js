// function displaylist() {
//     alert("Hello from a static file!");
    
//   }

const resultButton = document.getElementById("result-button");
const spinner = document.getElementById("spinner");
const resultContainer = document.getElementById("result-container");

resultButton.addEventListener("click", () => {
  spinner.style.display = "block";
  resultContainer.textContent = "Loading..."
    
  spinner.style.display = "none";
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("plan-form");
  const examDateInput = document.getElementById("exam_date");

  form.addEventListener("submit", function (e) {
    const today = new Date().toISOString().split("T")[0];
    if (examDateInput.value < today) {
      alert("Exam date cannot be in the past.");
      e.preventDefault();
    }
  });
});
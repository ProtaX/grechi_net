var submit_btn = document.getElementById("submit-btn")
var form = document.getElementById("participant-form")

var packages_count_out = document.getElementById("packages-count")
var meals_per_day_out_days = document.getElementById("meals-per-day-days")
var hungry_people_out_days = document.getElementById("hungry-people-days")
var package_volume_out_days = document.getElementById("package-volume-days")
var wb_per_meal_out_days = document.getElementById("wb-per-meal-days")

var packages_count_h = document.getElementById("packages_count_h")
var meals_per_day_h = document.getElementById("meals_per_day_h")
var wb_per_meal_h = document.getElementById("wb_per_meal_h")
var package_volume_h = document.getElementById("package_volume_h")
var hungry_people_h = document.getElementById("hungry_people_h")

submit_btn.onclick = function() {
    packages_count_h.value = packages_count_out.innerText;
    meals_per_day_h.value = meals_per_day_out_days.innerText;
    hungry_people_h.value = hungry_people_out_days.innerText;
    package_volume_h.value = package_volume_out_days.innerText;
    wb_per_meal_h.value = wb_per_meal_out_days.innerText;

    form.submit();
}
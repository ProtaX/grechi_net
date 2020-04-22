var packages_count_slider = document.getElementById("packages-count-slider")
var meals_per_day_slider = document.getElementById("meals-per-day-slider")
var packages_count_out = document.getElementById("packages-count")
var meals_per_day_out = document.getElementById("meals-per-day")

var quar_days_slider = document.getElementById("quar-days-slider")
var hungry_people_slider = document.getElementById("hungry-people-slider")
var quar_days_out = document.getElementById("quar-days")
var hungry_people_out = document.getElementById("hungry-people")

packages_count_slider.oninput = function() {
    packages_count_out.innerHTML = this.value;
}

meals_per_day_slider.oninput = function() {
    meals_per_day_out.innerHTML = this.value;
}

quar_days_slider.oninput = function() {
    quar_days_out.innerHTML = this.value;
}

hungry_people_slider.oninput = function() {
    hungry_people_out.innerHTML = this.value;
}

var packages_count_out = document.getElementById("packages-count")
var days_out = document.getElementById("days")
var packages_count_slider = document.getElementById("packages-count-slider")
var days_slider = document.getElementById("days-slider")

var hungry_people_slider_wb = document.getElementById("hungry-people-slider-wb")
var meals_per_day_slider_wb = document.getElementById("meals-per-day-slider-wb")
var package_volume_slider_wb = document.getElementById("package-volume-slider-wb");
var wb_per_meal_slider_wb = document.getElementById("wb-per-meal-slider-wb")
var meals_per_day_out_wb = document.getElementById("meals-per-day-wb")
var hungry_people_out_wb = document.getElementById("hungry-people-wb")
var package_volume_out_wb = document.getElementById("package-volume-wb")
var wb_per_meal_out_wb = document.getElementById("wb-per-meal-wb")

var hungry_people_slider_days = document.getElementById("hungry-people-slider-days")
var meals_per_day_slider_days = document.getElementById("meals-per-day-slider-days")
var package_volume_slider_days = document.getElementById("package-volume-slider-days");
var wb_per_meal_slider_days = document.getElementById("wb-per-meal-slider-days")
var package_volume_out_days = document.getElementById("package-volume-days")
var meals_per_day_out_days = document.getElementById("meals-per-day-days")
var hungry_people_out_days = document.getElementById("hungry-people-days")
var wb_per_meal_out_days = document.getElementById("wb-per-meal-days")

var dney = document.getElementById("dney")
var paketov = document.getElementById("paketov")

var wb_packages_enough = document.getElementById("wb-packages-enough")
var days_enough = document.getElementById("days-enough")

function calculateDaysEnough() {
    updateDaysEnough();
    var meals_per_day = parseInt(meals_per_day_out_wb.innerText);
    var package_value = parseInt(package_volume_out_wb.innerText);
    var hungry_people = parseInt(hungry_people_out_wb.innerText);
    var packages_count = parseInt(packages_count_out.innerText);
    var wb_per_meal = parseInt(wb_per_meal_out_wb.innerText);

    var res = Math.round(packages_count * package_value / meals_per_day / hungry_people / wb_per_meal);
    days_enough.innerHTML = res;
}

function calculateWbEnough() {

}

function updateDaysEnough() {
    var full_val = parseInt(days_enough.innerText);
    var val = full_val % 10;
    if (full_val == 0) {
        dney.innerHTML = "";
        days_enough.innerHTML = "сегодня";
        return;
    }
    if (full_val >= 10 && full_val <= 20) {
        dney.innerHTML = "дней";
        return;
    }
    if (val >= 2 && val <= 4) {
        dney.innerHTML = "дня";
    } else if (val == 1) {
        dney.innerHTML = "день";
    } else {
        dney.innerHTML = "дней";
    }
}

function updateWbEnough() {
    var val = parseInt(wb_packages_enough.innerText) % 10
    if (val == 1) {
        paketov.innerHTML = "пакет";
    } else if (val > 1 && val < 5) {
        paketov.innerHTML = "пакета";
    } else {
        paketov.innerHTML = "пакетов";
    }
}


// Days enough sliders
packages_count_slider.oninput = function() {
    calculateDaysEnough();
    packages_count_out.innerHTML = this.value;
}

meals_per_day_slider_days.oninput = function() {
    calculateDaysEnough();
    meals_per_day_out_days.innerHTML = this.value;
}

hungry_people_slider_days.oninput = function() {
    calculateDaysEnough();
    hungry_people_out_days.innerHTML = this.value;
}

package_volume_slider_days.oninput = function() {
    calculateDaysEnough();
    package_volume_out_days.innerHTML = this.value;
}

wb_per_meal_slider_days.oninput = function() {
    calculateDaysEnough();
    wb_per_meal_out_days.innerHTML = this.value
}

// Wb enough sliders
meals_per_day_slider_wb.oninput = function() {
    updateWbEnough();
    meals_per_day_out_wb.innerHTML = this.value;
}

hungry_people_slider_wb.oninput = function() {
    updateWbEnough();
    hungry_people_out_wb.innerHTML = this.value;
}

package_volume_slider_wb.oninput = function() {
    updateWbEnough();
    package_volume_out_wb.innerHTML = this.value;
}

days_slider.oninput = function() {
    updateWbEnough();
    days_out.innerHTML = this.value;
}

wb_per_meal_slider_wb.oninput = function() {
    updateWbEnough();
    wb_per_meal_out_wb.innerHTML = this.value
}
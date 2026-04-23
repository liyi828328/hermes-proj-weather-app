(function () {
    "use strict";

    const searchInput = document.getElementById("search-input");
    const searchBtn = document.getElementById("search-btn");
    const errorMsg = document.getElementById("error-msg");
    const cityList = document.getElementById("city-list");
    const weatherCard = document.getElementById("weather-card");

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.style.display = "block";
    }

    function hideError() {
        errorMsg.style.display = "none";
    }

    function hideCityList() {
        cityList.style.display = "none";
        cityList.innerHTML = "";
    }

    function hideWeatherCard() {
        weatherCard.style.display = "none";
    }

    async function searchCity(query) {
        hideError();
        hideCityList();
        hideWeatherCard();

        if (!query.trim()) {
            showError("请输入城市名称");
            return;
        }

        try {
            const resp = await fetch("/api/cities?q=" + encodeURIComponent(query.trim()));
            const data = await resp.json();

            if (data.code !== "OK") {
                showError(data.message || "查询失败，请稍后重试");
                return;
            }

            if (!data.data || data.data.length === 0) {
                showError("未找到匹配的城市");
                return;
            }

            renderCityList(data.data);
        } catch (e) {
            showError("网络错误，请检查网络连接");
        }
    }

    function renderCityList(cities) {
        cityList.innerHTML = "";
        cities.forEach(function (city) {
            const li = document.createElement("li");
            li.innerHTML =
                '<div class="city-main">' + escapeHtml(city.name) + "</div>" +
                '<div class="city-sub">' + escapeHtml(city.adm1 + " · " + city.adm2 + " · " + city.country) + "</div>";
            li.addEventListener("click", function () {
                getWeather(city.id, city.name);
            });
            cityList.appendChild(li);
        });
        cityList.style.display = "block";
    }

    async function getWeather(locationId, cityName) {
        hideError();
        hideCityList();

        try {
            const resp = await fetch("/api/weather?location=" + encodeURIComponent(locationId));
            const data = await resp.json();

            if (data.code !== "OK") {
                showError(data.message || "获取天气失败，请稍后重试");
                return;
            }

            renderWeather(data.data, cityName);
        } catch (e) {
            showError("网络错误，请检查网络连接");
        }
    }

    function renderWeather(w, cityName) {
        document.getElementById("city-name").textContent = cityName;
        document.getElementById("weather-temp").textContent = w.temp + "°C";
        document.getElementById("weather-text").textContent = w.text;
        document.getElementById("weather-wind").textContent = w.windDir;
        document.getElementById("weather-wind-scale").textContent = w.windScale + "级";
        document.getElementById("weather-humidity").textContent = w.humidity + "%";
        document.getElementById("weather-obs-time").textContent = w.obsTime;
        weatherCard.style.display = "block";
    }

    function escapeHtml(str) {
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    searchBtn.addEventListener("click", function () {
        searchCity(searchInput.value);
    });

    searchInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            searchCity(searchInput.value);
        }
    });
})();

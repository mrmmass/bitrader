const locales = ["en-GB", "ar-SA"];

function getCookie(cookieName) {
  const name = cookieName + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(';');
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) == ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) == 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}

function setCookie(cookieName, cookieValue, expirationDays) {
  const d = new Date();
  d.setTime(d.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
  const expires = "expires=" + d.toUTCString();
  document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";path=/";
}

function setLanguage(language) {
  setCookie("language", language, 30); // Save only the first two letters of the language code. Cookie expires in 30 days
}

function getLanguage() {
  const language = getCookie("language");
  if (language === "") {
    return "ar-SA"; // Default language if cookie is not set
  }
  return language;
}

function getFlagSrc(countryCode) {
  return /^[A-Z]{2}$/.test(countryCode) ?
    `https://flagsapi.com/${countryCode.toUpperCase()}/shiny/64.png` : "";
}

const dropdownBtn = document.getElementById("dropdown-btn");
const dropdownContent = document.getElementById("dropdown-content");

function setSelectedLocale(locale , system=false) {
  

  const intlLocale = new Intl.Locale(locale);
  const langName = new Intl.DisplayNames([locale], {
    type: "language",
  }).of(intlLocale.language);

  dropdownContent.innerHTML = "";

  const otherLocales = locales.filter((loc) => loc !== locale);
  otherLocales.forEach((otherLocale) => {
    const otherIntlLocale = new Intl.Locale(otherLocale);
    const otherLangName = new Intl.DisplayNames([otherLocale], {
      type: "language",
    }).of(otherIntlLocale.language);

    const listEl = document.createElement("li");
    listEl.innerHTML = `${otherLangName}<img src="${getFlagSrc(
      otherIntlLocale.region
    )}" />`;
    listEl.value = otherLocale;
    listEl.addEventListener("mousedown", function () {
      setSelectedLocale(otherLocale);
    });
    dropdownContent.appendChild(listEl);
  });

  dropdownBtn.innerHTML = `<img src="${getFlagSrc(
    intlLocale.region
  )}" />${langName}<span class="arrow-down"></span>`;

  if (!system && getLanguage()!== locale) {
    setLanguage(locale);
    window.location.reload();
  }

}


setSelectedLocale(locales[0] , true);
const browserLang = new Intl.Locale(navigator.language).language;
for (const locale of locales) {
  const localeLang = new Intl.Locale(locale).language;
  if (localeLang === browserLang) {
    setSelectedLocale(locale , true);
  }
}


setSelectedLocale(getLanguage() , true);

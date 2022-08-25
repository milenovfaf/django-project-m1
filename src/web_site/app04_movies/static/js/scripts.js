// Параметры (жанр, года) и url передали сюда в функциях ниже
function ajaxSend(url, params) {
    // Отправляем запрос с помощью fetch, но можно использовать Ajax Джаквэри но я не ебу как
    fetch(`${url}?${params}`, {
        // Метод отправки
        method: 'GET',
        // Заголовок Content-Type который будет вправлен
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        // В первом промизе преабразуев json
        .then(response => response.json())
        // Затем json передаём функции render
        .then(json => render(json))
        // Если произойдёт ошибка выведем её в консоль
        .catch(error => console.error(error))
}



// // C помощью querySelector ищем форму по имени filter
// const forms = document.querySelector('form[name=filter]');
//
// // Когда у формы бует вызван метод submit, запустим функцию которая принимает Event
// forms.addEventListener('submit', function (e) {
//     // Получаем данные из формы
//     // Убираем дефолтное значение которое происходит при нажатии submit
//     // это отправление данных формы и перезагрузка страницы
//     e.preventDefault(); // тут мы блокируем это действие
//     // В переменную url пихаем инфу (url) из атрибута action нашей формы
//     let url = this.action; // this указывает на форму action её атрибут
//     // С помощью URLSearchParams выстраиваем параметры которым будем передавать url
//     // С помощью FormData передаём форму переданную в URLSearchParams
//     // И преобразовываем полученные данные в строку с помощью toString()
//     // Таким образом получаем параметры (года, жанры)
//     let params = new URLSearchParams(new FormData(this)).toString();
//     // Передаём в функцию ajaxSend url и параметры params
//     ajaxSend(url, params);
// });

// Рендер принемает json сверу
function render(data) {
    // C Помощью библиотеки hogan (которую подключили в base.html) компилируем шаблон html (переменная)
    let template = Hogan.compile(html);
    // Вызвая метод render полученного шаблона передаём тот json который пришёл от сервера
    let output = template.render(data);
    // Находим блок div в котором вставляются блоки с фольмом
    const div = document.querySelector('.left-ads-display>.row');
    // И в этот div вставляем результат. Конец.
    div.innerHTML = output;
}


// Этот html из movie_list там где рендерится один блок фильма
// С помощью синтаксиса данного шаблонизатора перебираем список movies и в нужные места выводм информацию
// Там где выводится изображение, так как получаем просто url изображения нужно добавить url media/
// Передавая url, title и tagline будем выводить это в нужные места шаблона
let html = '\
{{#movies}}\
    <div class="col-md-4 product-men">\
        <div class="product-shoe-info editContent text-center mt-lg-4">\
            <div class="men-thumb-item">\
                <img src="media/{{ poster }}" class="img-fluid" alt="">\
            </div>\
            <div class="item-info-product">\
                <h4 class="">\
                    <a href="/{{ url }}" class="editContent">\
                    {{ title }}\
                    </a>\
                </h4>\
                <div class="product_price">\
                    <div class="grid-price">\
                        <span class="money editContent">{{ tagline }}</span>\
                    </div>\
                </div>\
                <ul class="stars">\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a></li>\
                </ul>\
            </div>\
        </div>\
    </div>\
{{/movies}}'  // Закрывам цикл


// Добавление звёзд рейтинга
// С помощью querySelector ищем форму с именем rating
const rating = document.querySelector('form[name=rating]');
// Тогда у этой формы вызовится событие change
rating.addEventListener('change', function () {
    // Получаем данные из формы
    // Создавая FormData и передав форму мы получаем значения всех полей
    let data = new FormData(this);
    // На url из нашей формы будем отправлять post запрос передавая в теле (body) нашу data
    // ПИЗДЕЦ где `${this.action}` не кавычки одинарные а апострафы, ЕБАНУТЬСЯ
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        // при успешном или нет ответе появится соответствующее соббщение
        .then(response => alert('Рейтинг установлен'))
        .catch(error => alert('Ошибка'))
});

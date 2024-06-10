//1. ѕри изменении значени€ в input с id = "from", значение содержащеес€ в нем должно моментально отображатьс€ в span.“о есть при печати в input'е тег span также должен мен€тьс€.
console.log("Hello");
let element = document.querySelector("#from");
element.addEventListener('input', (e) => {
    element.nextElementSibling.innerHTML = element.value;
})


//2. ѕри клике на кнопку с классом messageBtn необходимо элементу с классом message:
//- добавить два класса: animate_animated и animate_fadeInLeftBig
//- поставить данному элементу стиль visibility в значение 'visible'.
document.querySelector(".messageBtn").addEventListener('click', () => {
    element = document.querySelector(".message");
    element.classList.add("animate_animated", "animate_fadeInLeftBig");
    element.style.visibility = 'visible';
    console.log(element);
})




//3. Ќеобходимо при отправке формы проверить, заполнены ли все пол€ в этой форме.≈сли какое - либо поле не заполнено, форма не должна отправл€тьс€, также должны быть подсвечены незаполненные пол€(необходимо поставить класс error незаполненным пол€м). ак только пользователь начинает заполн€ть какое - либо поле, необходимо, при вводе в данное поле, произвести проверку:
//- ≈сли поле пустое, необходимо данное поле подсветить(поставить класс error данному полю).
//- ≈сли поле было чем - либо заполнено, подсветку(класс error) необходимо убрать.


document.forms[0].addEventListener('input', (e) => {
    if (document.forms[0].elements[0].value == "") {
        document.forms[0].elements[0].classList.add("error");
    } else {
        document.forms[0].elements[0].classList.remove("error");
    }
    if (document.forms[0].elements[1].value == "") {
        document.forms[0].elements[1].classList.add("error");
    } else {
        document.forms[0].elements[1].classList.remove("error");
    }
    console.log(document.forms[0].elements[0].classList);
    console.log(document.forms[0].elements[1].classList);
})

document.forms[0].addEventListener('click', (e) => {
    if (document.forms[0].elements[0].value == "") {
        document.forms[0].elements[0].classList.add("error");
    } else {
        document.forms[0].elements[0].classList.remove("error");
    }
    if (document.forms[0].elements[1].value == "") {
        document.forms[0].elements[1].classList.add("error");
    } else {
        document.forms[0].elements[1].classList.remove("error");
    }
    console.log(document.forms[0].elements[0].classList);
    console.log(document.forms[0].elements[1].classList);
    if ((e.target.tagName == "BUTTON") & (document.forms[0].elements[0].value != "") & (document.forms[0].elements[1].value != "")) {
        console.log("Send to Server!");
    }
    e.preventDefault();
})

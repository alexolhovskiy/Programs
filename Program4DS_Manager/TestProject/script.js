//1. ��� ��������� �������� � input � id = "from", �������� ������������ � ��� ������ ����������� ������������ � span.�� ���� ��� ������ � input'� ��� span ����� ������ ��������.
console.log("Hello");
let element = document.querySelector("#from");
element.addEventListener('input', (e) => {
    element.nextElementSibling.innerHTML = element.value;
})


//2. ��� ����� �� ������ � ������� messageBtn ���������� �������� � ������� message:
//- �������� ��� ������: animate_animated � animate_fadeInLeftBig
//- ��������� ������� �������� ����� visibility � �������� 'visible'.
document.querySelector(".messageBtn").addEventListener('click', () => {
    element = document.querySelector(".message");
    element.classList.add("animate_animated", "animate_fadeInLeftBig");
    element.style.visibility = 'visible';
    console.log(element);
})




//3. ���������� ��� �������� ����� ���������, ��������� �� ��� ���� � ���� �����.���� ����� - ���� ���� �� ���������, ����� �� ������ ������������, ����� ������ ���� ���������� ������������� ����(���������� ��������� ����� error ������������� �����).��� ������ ������������ �������� ��������� ����� - ���� ����, ����������, ��� ����� � ������ ����, ���������� ��������:
//- ���� ���� ������, ���������� ������ ���� ����������(��������� ����� error ������� ����).
//- ���� ���� ���� ��� - ���� ���������, ���������(����� error) ���������� ������.


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

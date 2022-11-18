
    const question = document.querySelectorAll('.faq');

    question.forEach(faq => {
        faq.addEventListener("click", () => {
            faq.classList.toggle("active");
        })
    })
document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

            // INSTITUTION FILTER
            const selectedCategoryIDs = [...document.querySelectorAll("div[data-step='1'] input:checked")].map(input => input.value);
            const selectedCategoryIDsList = [...document.querySelectorAll("div[data-step='1'] input:checked")];
            const selectedCategories = [];
            for (let sel of selectedCategoryIDsList) {
                selectedCategories.push(sel.nextElementSibling.nextElementSibling.innerText);
            }
            const instDivs = document.querySelectorAll("div[data-step='3'] div.form-group--checkbox");

            for (let div of instDivs) {
                div.style.display = "none";
            }

            for (let div of instDivs) {
                const institutionCategoryIDs = div.dataset.categoryIds.split(", ");
                const matchesCriteria = selectedCategoryIDs.every(x => institutionCategoryIDs.includes(x));

                if (matchesCriteria) {
                    div.style.display = "block";
                }
            }

            // BAG AMOUNT - STEP 2
            const formQuantity = document.querySelector("input[name='bags']");

            // FORM FIELDS FROM STEP 4
            const formAddress = document.querySelector("div[data-step='4'] input[name='address']");
            const formCity = document.querySelector("div[data-step='4'] input[name='city']");
            const formPostcode = document.querySelector("div[data-step='4'] input[name='postcode']");
            const formPhone = document.querySelector("div[data-step='4'] input[name='phone']");
            const formDate = document.querySelector("div[data-step='4'] input[name='data']");
            const formTime = document.querySelector("div[data-step='4'] input[name='time']");
            const formComment = document.querySelector("div[data-step='4'] textarea[name='more_info']");
            const formChosenInstitutionID = document.querySelector("input[type='radio']:checked");
            const formChosenInstitution = formChosenInstitutionID.nextElementSibling.nextElementSibling.firstElementChild;


            // proper "worki" word
            function bagWord(bagAmount) {
                if (bagAmount.value[bagAmount.value.length - 1] == 0 || bagAmount.value[bagAmount.value.length - 1] >= 5) {
                    return "worków"
                } else if (bagAmount.value > 9 && formQuantity.value < 20) {
                    return "worków"
                } else if (bagAmount.value[bagAmount.value.length - 1] == 1 || bagAmount.value == 1) {
                    return "worek"
                } else {
                    return "worki"
                }
            }


            // INPUT FORM FIELDS TO FORM SUMMARY - STEP 5
            document.querySelector("#final-summary").innerText = `${formQuantity.value} ${bagWord(formQuantity)} w kategoriach: ${selectedCategories.toString()}`;
            document.querySelector("#final-institution").innerText = `Dla fundacji - ${formChosenInstitution.innerText}`;

            document.querySelector("#final-address").innerText = formAddress.value;
            document.querySelector("#final-city").innerText = formCity.value;
            document.querySelector("#final-postcode").innerText = formPostcode.value;
            document.querySelector("#final-phone").innerText = formPhone.value;
            document.querySelector("#final-date").innerText = formDate.value;
            document.querySelector("#final-time").innerText = formTime.value;
            document.querySelector("#final-comment").innerText = formComment.value;

        }

        // /**
        //  * Submit form
        //  *
        //  * TODO: validation, send data to server
        //  */
        // submit(e) {
        //     e.preventDefault();
        //     this.currentStep++;
        //     this.updateForm();
        // }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

});



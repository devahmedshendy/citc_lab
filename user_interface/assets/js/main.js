$(document).ready(function() {
  var page_name = document.title.split(" - ")[0];
  console.log(page_name);

  if (page_name === "Login") {


  } else if (page_name === "Home") {
    let patients = getListOfPatients();

    displayPatientsElements(patients);

    $('#search-box').on("keyup keypress", (event) => {
      let targetElement = $(event.target);

      if (targetElement.val().length > 0) {
        $('#search-result').text(event.target.value);

      } else if (targetElement.val().length === 0 && $('#search-result li').length === 0) {
        displayPatientsElements(patients);
      }

    });

    $('#search-result').on("mouseover mouseout", (event) => {
      toggleClass(event.target, 'active');
    });

    /* Home page specific functions */
    function getListOfPatients() {
      return [
        {
          name: "Yasser Rahman Shokry",
          age: 43
        },
        {
          name: "Yomna Mostafa Mohamed",
          age: 82
        },
        {
          name: "Mohamed Sameh Rushdy",
          age: 28
        },
        {
          name: "Ramiz Hamed Al Morshdy",
          age: 50
        },
        {
          name: "Mai Mansour Himdan",
          age: 39
        }
      ];
    }

    /*
      <a href="#" target="_blank">
        <li class="list-group-item justify-content-between">
          Mohamed Sameh Rushdy
          <span>25 Years</span>
        </li>
      </a>
    */
    function displayPatientsElements(patients) {
      $("#search-result").html('')

      patients.forEach((patient) => {
        let anchorElement = $("<a></a>").attr({
          "target": "_blank",
          "href": ""
        });

        let listElement = $("<li></li>")
          .addClass("list-group-item justify-content-between border-right-0 border-left-0 border-bottom-0")
          .text(patient.name);

        let spanElement = $("<span></span>")
          .text(`${patient.age}y`);

        spanElement.appendTo(listElement);
        listElement.appendTo(anchorElement);

        anchorElement.appendTo("#search-result");
      });
    }

  } else if (page_name === "Patient Profile") {
    console.log("Patient Profile Page");

  } else if (page_name === "New Patient") {
    console.log("New Patient Page");
  }



  /* Global Functions */
  function toggleClass(item, className) {
    $(item).toggleClass(className);
  }

  function displayPatientCBCElements(patient) {

  }

});

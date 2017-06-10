$(document).ready(function() {
    var page_name = document.title.split(" - ")[0];
    console.log(page_name);

    // === Home Page =============================================================
    if (page_name === "Home") {
        let patients_list = []

        // === Home Page Initialization ====
        $.get('/patient?json=True', (res) => {
          res = JSON.parse(res)

          res.forEach((patient) => {
            patients_list.push(patient)
          })

          displayPatientsElements(patients_list);
        });

        $("#search-result").slimScroll({
            wheelStep: 3,
            alwaysVisible: true,
            railVisible: true,
            height: '400px',
        });


        // === Home Page Event Handlers ====
        $('#search-box').on("keyup keypress", (event) => {
          let targetElement = $(event.target);

          if (targetElement.val().length > 0) {
            $('#search-result').text(event.target.value);

          } else if (targetElement.val().length === 0 && $('#search-result li').length === 0) {
            displayPatientsElements(patients_list);
          }
        });


        $('#search-result').on("mouseover mouseout", (event) => {
          $(event.target).toggleClass('active');
        });


        // === Home Page Functions ====
        function displayPatientsElements(patients) {
          $("#search-result").html('')
          /*
            <a href="#" target="_blank">
              <li class="list-group-item justify-content-between">
                Mohamed Sameh Rushdy
                <span>25 Years</span>
              </li>
            </a>
          */
          patients.forEach((patient) => {
            let anchorElement = $("<a></a>").attr({
              "href": `/analysis/personal_id/${patient.personal_id}`
            });

            let listElement = $("<li></li>")
              .addClass("list-group-item justify-content-between border-right-0 \
                         border-left-0 border-bottom-0")
              .text(patient.name);

            let spanElement = $("<span></span>")
              .text(`${patient.updated_at}`);

            spanElement.appendTo(listElement);
            listElement.appendTo(anchorElement);
            anchorElement.appendTo("#search-result");
          });
        }
    }


    // === Analysis Profile Page ===============================================
    if (page_name === "Analysis Profile") {
        let patient_id = $("#patient_id").text();

        // === Analysis Profile Initialization ====
        $.get(`/analysis/personal_id/${patient_id}?json=True`, (res) => {
            res = JSON.parse(res)

            displayCBCAnalyzesElements(res)
            console.log(res);
        })
        .fail((err) => {
            console.log(err);
        })

        $('#patient_analyzes_list').slimScroll({
            wheelStep: 3,
            alwaysVisible: true,
            railVisible: true,
            height: '400px',
        });


        // === Analysis Profile Event Handlers ====
        // CBC Button Clicked
        $("#add_cbc_button").click((event) => {
            console.log("Form submitted");

            $("#add_cbc_form").submit();
            // console.log(wbc);
        });

        // Submit CBC Form
        $("#add_cbc_form").submit((event) => {
            event.preventDefault();

            var submitted_data       = $(event.target).serialize();
            var submitted_data_array = $(event.target).serializeArray();
            var add_cbc_form         = $("#add_cbc_form");
            var action_url           = $("#add_cbc_form").attr("action");

            var cbc_analysis_form_data = JSON.stringify({
                "comment" : $("#comment").val(),
                "WCB"     : $("#WCB").val(),
                "HGB"     : $("#HGB").val(),
                "MCV"     : $("#MCV").val(),
                "MCH"     : $("#MCH").val()
            })

            $.ajax({
                method: 'POST',
                url: `${action_url}`,
                contentType: 'application/json',
                data: cbc_analysis_form_data
            })
            .done((data) => {
                data = JSON.parse(data);

                if (data.hasOwnProperty("error")) {
                    errors_list  = data["error"]

                    /*
                    <div class="row">
                      <div class="offset-3 col-6">
                        <div class="alert alert-danger" role="alert">
                          <ul>
                              <li><small>error<small></li>
                          </ul>
                        </div>
                      </div>
                    </div>
                    */
                    let row   = $(`<div class='row'></div>`)
                    let col   = $(`<div class='offset-1 col-10'></div>`).appendTo(row)
                    let alert = $(`<div class='alert alert-danger' role='alert'></div>`).appendTo(col)
                    let ul    = $(`<ul></ul>`).appendTo(alert)

                    errors_list.forEach((message) => {
                        console.log(message);
                        let li = $(`<li>${message}</li>`).appendTo(ul);
                    });

                    $(row).insertBefore("#add_cbc_form");

                } else if (data.hasOwnProperty("success")) {
                    $("#cbcModal").modal("hide");
                    success_message = data["success"][0]

                    let success_row   = $(`
                        <div class='row'>
                            <div class='offset-3 col-6'>
                                <div class='alert alert-success alert-dismissible fade show' role='alert'>
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                    ${success_message}
                                </div>
                            </div>
                        </div>
                    `);

                    $("#header-container").prepend(success_row);

                    $.get(`/analysis/personal_id/${patient_id}?json=True`, (res) => {
                        res = JSON.parse(res)

                        displayCBCAnalyzesElements(res)
                        console.log(res);
                    })
                    .fail((err) => {
                        console.log(err);
                    });
                }

            })
            .fail((err) => {
                console.log(err);
            });
        });


        // === Analysis Profile Page Functions ====
        function displayCBCAnalyzesElements(cbc_analyzes) {
            var accordion = $("#patient_analyzes_list #accordion")
                                .first()
                                .html('')

            cbc_analyzes.forEach((cbc) => {
                let card = $(`
                    <div class="card">
                      <div class="card-header" role="tab" id="heading${cbc['id']}">
                        <a href="#collapse${cbc['id']}" data-toggle="collapse" data-parent="#accordion" aria-expanded="true" aria-controls="collapse${cbc['id']}" class="list-group-item-action flex-column align-items-start">
                          <div class="d-flex w-100 justify-content-between">
                            <!-- "analysis_type": "CBC Analysis" -->
                            <h6 class="mb-1">CBC Analysis</h6>
                            <!-- "created_at": "2017-05-29" -->
                            <small>${cbc['updated_at']}</small>
                          </div>
                          <!-- "comment": "Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit." -->
                          <p class="mb-1">Comment: <span>${cbc["comment"]}</span></p>
                          <small class="text-muted">Approved by Dr.Zizo.</small>
                        </a>
                      </div>

                      <div id="collapse${cbc["id"]}" class="collapse" role="tabpanel" aria-labelledby="heading${cbc["id"]}">
                        <div class="card-block">
                          <div class="row">
                            <div class="container">
                              <div class="row">
                                <div class="col align-self-center text-center">
                                  <a href="#">Edit</a> | <a href="#">Delete</a>
                                </div>
                              </div>
                            </div>

                            <div class="col-12">
                              <table class="table table-sm">
                                <thead>
                                  <tr>
                                    <th>Item</th>
                                    <th>Value</th>
                                    <th>Normal</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr>
                                    <th scope="row">WBC</th>
                                    <!-- "WCB": "2.19" -->
                                    <td>${cbc["WCB"]}</td>
                                    <td>3.70 - 10.10</td>
                                  </tr>
                                  <tr>
                                    <th scope="row">HGB</th>
                                    <!-- "HGB": "12.9" -->
                                    <td>${cbc["HGB"]}</td>
                                    <td>12.9 - 15.9</td>
                                  </tr>
                                  <tr>
                                    <th scope="row">MCV</th>
                                    <!-- "MCV": "82.2" -->
                                    <td>${cbc["MCV"]}</td>
                                    <td>81.1 - 96.0</td>
                                  </tr>
                                  <tr>
                                    <th scope="row">MCH</th>
                                    <!-- "MCH": "27.3" -->
                                    <td>${cbc["MCH"]}</td>
                                    <td>27.0 - 31.2</td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                  `)
                  .appendTo(accordion)

              })
        }
    }
});

$(document).ready(() => {
  // === Medical Profile Page ===============================================

    //-----------------------------------------
    //
    // Medical Profile Initialization
    //-----------------------------------------
    var cbc = {
      "id"      : 0,
      "wcb"     : 0,
      "hgb"     : 0,
      "mcv"     : 0,
      "mch"     : 0,
      "comment" : "---",
    }

    var patient_id = $("#patient_personal_details").attr("data-patient-id");
    displayCBCAnalyzesElements();

    $('#patient_analyzes_list').slimScroll({
        wheelStep: 3,
        alwaysVisible: true,
        railVisible: true,
        height: '400px',
    });

    //-----------------------------------------
    //
    // Handling Process of Adding New CBC
    //-----------------------------------------
    // CBC Add Link -> Clicked
    $(document).on('click', '#add_cbc_link', (event) => {
        var add_cbc_link = $(event.target)

        // var patient_id = $("#patient_personal_details").attr('data-patient-id')
        var add_cbc_modal = createModalToAddCBC(patient_id)

        $(add_cbc_modal).modal('toggle');
    });

    // CBC Add Modal -> Add Button Clicked
    $(document).on("click", "#add_cbc_button", (event) => {
        var submitted_data       = $(event.target).serialize();
        var submitted_data_array = $(event.target).serializeArray();
        var add_cbc_form         = $("#add_cbc_form");
        var add_cbc_modal         = $(add_cbc_form).closest(".modal");
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
            url: action_url,
            contentType: 'application/json',
            data: cbc_analysis_form_data
        })
        .done((data) => {
            data = JSON.parse(data);

            if (data.hasOwnProperty("error")) {
                let errors_list  = data["error"]

                clearAlert("#add_cbc_success")
                showErrorAlert("#add_cbc_error", errors_list)

            } else if (data.hasOwnProperty("success")) {
                $(add_cbc_modal).modal("hide");

                displayCBCAnalyzesElements();

                let success_message = data["success"]
                showSuccessAlert("#add_cbc_success", success_message);
            }
        })
        .fail((err) => {
            console.log(err);
        });
    });

    //-----------------------------------------
    //
    // Handling Process of Editing CBC
    //-----------------------------------------
    // CBC Edit Link -> Clicked
    $(document).on('click', '[data-cbc-edit]', (event) => {
        var edit_cbc_link = $(event.target)

        setGlobalCBC(...getCBCDataFromLink(edit_cbc_link))

        var patient_id = $("#patient_personal_details").attr('data-patient-id')
        var edit_cbc_modal = createModalWithEditCBCForm(patient_id, "cbc", cbc)

        $(edit_cbc_modal).modal('toggle');
    });

    // CBC Edit Modal -> Save Button Clicked
    $(document).on('click', "[data-button-type=save]", (event)=> {
        var edit_cbc_form  = $("#edit_cbc_form");
        var action_url = edit_cbc_form.attr("action");

        var edit_cbc_link = $(`#collapse${cbc["id"]} [data-cbc-edit]`);

        setGlobalCBC(id = cbc.id, ...getCBCDataFromEditCBCForm(edit_cbc_form));

        var submitted_data = JSON.stringify({
            "comment" : cbc.comment,  "WCB"     : cbc.wcb,
            "HGB"     : cbc.hgb,      "MCV"     : cbc.mcv,
            "MCH"     : cbc.mch });

        // Send CBC data to save into database
        $.ajax({
          method: 'POST',
          url: action_url,
          contentType: 'application/json',
          data: submitted_data
        })
        .done((messages) => {
            messages = JSON.parse(messages);

            if (messages.hasOwnProperty("error")) {
                let errors_list = messages["error"];

                clearAlert('#add_cbc_success');
                showErrorAlert('#edit_cbc_error', errors_list);

            } else if (messages.hasOwnProperty("success")) {
                submitted_data = JSON.parse(submitted_data);

                changeCBCCardWithSavedCBCData(submitted_data);

                $(edit_cbc_modal).modal('hide');

                let success_message = messages['success'];
                showSuccessAlert("#add_cbc_success", success_message);
            }
        })
        .fail((err) => {
            console.log(err);
        });

    });

    //-----------------------------------------
    //
    // Handling Delete CBC Process
    //-----------------------------------------
    // CBC Delete Link -> Clicked
    $(document).on('click', '[data-cbc-delete]', (event) => {
        var cbc_id = $(event.target).attr("data-cbc-id");
        var confirm_delete_cbc_modal = createModalToConfirmCBCDelete(cbc_id);

        $(confirm_delete_cbc_modal).modal('show');
    });

    // Confirm Delete CBC Modal -> Form Submitted
    $(document).on('click', "#confirm_delete_cbc_button", (event) => {
        event.preventDefault();

        var confirm_delete_cbc_button = $(event.target);
        var analysis_id               = $(confirm_delete_cbc_button).attr(`data-cbc-id`);

        // Send Delete as a GET request to the server
        $.ajax({
          method: 'POST',
          url: `/analyzes/cbc/${analysis_id}/delete`,
        })
        .done((messages) => {
            var messages = JSON.parse(messages);

            if (messages.hasOwnProperty("error")) {
                let errors_list = messages["error"];

                clearAlert("#add_cbc_success");
                showErrorAlert("#confirm_delete_cbc_error", errors_list);

            } else if (messages.hasOwnProperty("success")) {
                $(`div[id^=confirm_delete_cbc]`).modal('hide');

                displayCBCAnalyzesElements();

                let success_message = messages['success']
                showSuccessAlert("#add_cbc_success", success_message);
            }
        })
        .fail((err) => {
            console.log(err);
        });

    });

    //-----------------------------------------
    //
    // Handling Modal Hidden Event
    //-----------------------------------------
    // Confirm CBC Delete Modal -> Hidden
    $(document).on('hidden.bs.modal', 'div[id^=confirm_delete_cbc]', (event) => {
      $(event.target).remove();
      resetGlobalCBC();
    });

    // Add CBC Modal -> Hidden
    $(document).on('hidden.bs.modal', '#add_cbc_modal', (event) => {
      // $("#add_cbc_form")[0].reset();
      $(event.target).remove();
      resetGlobalCBC();
    });

    // Edit CBC Modal -> Hidden
    $(document).on('hidden.bs.modal', '#edit_cbc_modal', (event) => {
      $(event.target).remove();
      resetGlobalCBC();
    });

    //-----------------------------------------
    //
    // Analysis Profile Page Functions
    //-----------------------------------------
    function displayCBCAnalyzesElements() {
      $.get(`/patients/${patient_id}/analyzes?json=True`, (res) => {
          var cbc_analyzes_list = JSON.parse(res);

          let accordion = $("#patient_analyzes_list #accordion").html('')

          cbc_analyzes_list.forEach((cbc) => {
              createCBCCard(patient_id, "cbc", cbc).appendTo(accordion)
          });
      })
      .fail((err) => {
          console.log(err);
      });
    }

    function changeCBCCardWithSavedCBCData(submitted_data) {
        let edit_cbc_link = $(`#collapse${cbc["id"]} [data-cbc-edit]`);
        let cbc_table     = $(`#table-${cbc["id"]}`)

        for (key in submitted_data) {
          let data_element = `data-cbc-${key.toLowerCase()}`

          $(edit_cbc_link).attr(`${data_element}`, submitted_data[key])

          $(cbc_table).find(`[${data_element}]`)
                      .text(submitted_data[key])
                      .attr(`${data_element}`, submitted_data[key]);
        }

        $(`#collapse${cbc["id"]} span[data-cbc-comment]`)
            .text(submitted_data["comment"]);

    }


    function getCBCDataFromLink(link) {
        cbc_data =  [ $(link).attr("data-cbc-id"),
                      $(link).attr("data-cbc-wcb"),
                      $(link).attr("data-cbc-hgb"),
                      $(link).attr("data-cbc-mcv"),
                      $(link).attr("data-cbc-mch"),
                      $(link).attr("data-cbc-comment") ];

        return cbc_data;
    }

    function getCBCDataFromEditCBCForm(edit_cbc_form) {
        cbc_data = [ $(edit_cbc_form).find("#WCB").val(),
                     $(edit_cbc_form).find("#HGB").val(),
                     $(edit_cbc_form).find("#MCV").val(),
                     $(edit_cbc_form).find("#MCH").val(),
                     $(edit_cbc_form).find("#comment").val() ];

         return cbc_data;
    }


    function setGlobalCBC(id, wcb, hgb, wcv, wch, comment) {
        cbc = { "id"      : id,   "wcb"     : wcb,
                "hgb"     : hgb,  "mcv"     : wcv,
                "mch"     : wch,  "comment" : comment}
    }

    function resetGlobalCBC() {
        cbc = { "id"      : 0,    "wcb"     : 0,
                "hgb"     : 0,    "mcv"     : 0,
                "mch"     : 0,    "comment" : "---"  }
    }


    // Create Alert to Display Error/Success Messages
    function showErrorAlert(alert_id, errors_list) {
      var error_alert = createErrorAlert(errors_list);
      $(alert_id).html(error_alert);
    }

    function createErrorAlert(errors_list) {
        var ul_of_errors    = $(`<ul></ul>`);

        errors_list.forEach((message) => {
            let li = $(`<li>${message}</li>`).appendTo(ul_of_errors);
        });

        var error_alert = createAlert("error", ul_of_errors);
        return error_alert;
    }

    function showSuccessAlert(alert_id, success_message) {
      var success_element = createSuccessAlert(success_message);
      $(alert_id).html($(success_element));
    }

    function createSuccessAlert(success_message) {
        var success_message = $(`<p>${success_message}</p>`)

        var success_alert = createAlert("success", success_message)
        return success_alert;
    }

    function createAlert(alert_type, alert_messages) {
        var alert = null;

        if (alert_type === "error") {
            alert = $(`
                <div class='offset-1 col-10'>
                    <div class='alert alert-danger' role='alert'>
                        ${alert_messages.html()}
                    </div>
                </div>
            `)

        } else if (alert_type === "success") {
            alert = $(`
                <div class='offset-3 col-6'>
                    <div class='alert alert-success alert-dismissible fade show' role='alert'>
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        ${alert_messages.html()}
                    </div>
                </div>
            `);
        }

        return alert;
    }

    function clearAlert(alert_id) {
      $(alert_id).html('');
    }


    // Create Card for CBC Data
    function createCBCCard(patient_id, analysis_type, analysis_data) {
        var comment_element = ''
        var approved_element = ''
        var cbc_edit_options = ''

        if (analysis_data["approved"] == false) {
            comment_element = `
                <p class="text-muted">Not Approved Yet.</p>
            `

            cbc_edit_options = `
                <div id="cbc_edit_options" class="col align-self-center text-center">
                  <a href="#"
                      data-cbc-edit
                      data-cbc-id="${analysis_data["id"]}"
                      data-cbc-comment="${analysis_data["comment"]}"
                      data-cbc-wcb="${analysis_data["WCB"]}"
                      data-cbc-hgb="${analysis_data["HGB"]}"
                      data-cbc-mcv="${analysis_data["MCV"]}"
                      data-cbc-mch="${analysis_data["MCH"]}"
                      data-toggle="modal"
                      data-target="#edit_cbc_modal">
                      Edit
                  </a>
                  |
                  <a href="#"
                      data-cbc-delete
                      data-cbc-id="${analysis_data["id"]}"
                      data-cbc-comment="${analysis_data["comment"]}"
                      data-cbc-wcb="${analysis_data["WCB"]}"
                      data-cbc-hgb="${analysis_data["HGB"]}"
                      data-cbc-mcv="${analysis_data["MCV"]}"
                      data-cbc-mch="${analysis_data["MCH"]}"
                      data-toggle="modal"
                      data-target="#confirm_delete_cbc${analysis_data["id"]}_modal">
                      Delete
                  </a>
                </div>
            `

        } else if (analysis_data["approved"] == true){
            comment_element = `
                <p data-cbc-doctor-name class="text-muted">Approved By Dr. <span style="font-weight: bold">${analysis_data["comment_doctor"]}</span>.</p>
                <p>
                  <span id="cbc${analysis_data["id"]}_comment" data-cbc-comment>${analysis_data["comment"]}</span>
                </p>
            `

            approved_element = `
                <span class="badge badge-success">Approved</span>
            `

            cbc_edit_options = `
                <div id="cbc_edit_options" class="col align-self-center text-center">
                    <a href="#"
                        data-cbc-delete
                        data-cbc-id="${analysis_data["id"]}"
                        data-cbc-comment="${analysis_data["comment"]}"
                        data-cbc-wcb="${analysis_data["WCB"]}"
                        data-cbc-hgb="${analysis_data["HGB"]}"
                        data-cbc-mcv="${analysis_data["MCV"]}"
                        data-cbc-mch="${analysis_data["MCH"]}"
                        data-toggle="modal"
                        data-target="#confirm_delete_cbc${analysis_data["id"]}_modal">
                        Delete
                    </a>
                </div>
            `
        }

        let card_header = `
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">
                CBC Analysis - <small>${analysis_data["id"]}</small>
              </h6>
              ${approved_element}
              <small>${analysis_data["updated_at"]}</small>
            </div>

            <div class="d-flex w-100 justify-content-between">
              <a href="#collapse${analysis_data["id"]}" data-toggle="collapse" data-parent="#accordion" aria-expanded="true" aria-controls="collapse${analysis_data["id"]}" class="flex-column align-items-start btn btn-link btn-sm">
                Show Data
              </a>

              <a href="/patients/${patient_id}/analyzes/cbc/${analysis_data["id"]}/pdf"
                  class="mb-1 btn btn-link btn-sm"
                  target="_blank"
                  data-cbc-options-link="print_pdf">PDF
              </a>
            </div>
        `

        let card_block = `
            <div class="row">
              <div class="container">
                <div class="row">
                  ${cbc_edit_options}
                </div>
              </div>

              <div class="col-12">
                <hr>
                <div class="mb-1">
                  ${comment_element}
                </div>

                <table id="table-${analysis_data["id"]}" class="table table-sm">
                  <thead>
                    <tr>
                      <th>Item</th>
                      <th>Value</th>
                      <th>Normal</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">WCB</th>
                      <!-- "WCB": "2.19" -->
                      <td data-cbc-wcb=${analysis_data["WCB"]}>${analysis_data["WCB"]}</td>
                      <td>3.70 - 10.10</td>
                    </tr>
                    <tr>
                      <th scope="row">HGB</th>
                      <!-- "HGB": "12.9" -->
                      <td data-cbc-hgb=${analysis_data["HGB"]}>${analysis_data["HGB"]}</td>
                      <td>12.9 - 15.9</td>
                    </tr>
                    <tr>
                      <th scope="row">MCV</th>
                      <!-- "MCV": "82.2" -->
                      <td data-cbc-mcv=${analysis_data["MCV"]}>${analysis_data["MCV"]}</td>
                      <td>81.1 - 96.0</td>
                    </tr>
                    <tr>
                      <th scope="row">MCH</th>
                      <!-- "MCH": "27.3" -->
                      <td data-cbc-mch=${analysis_data["MCH"]}>${analysis_data["MCH"]}</td>
                      <td>27.0 - 31.2</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
        `

        let card = createCard(card_header, `heading${analysis_data['id']}`, card_block, `collapse${analysis_data["id"]}`)

        // let confirm_delete_cbc_modal = createModalToConfirmCBCDelete(patient_id, analysis_type, analysis_data["id"])
        //                                   .appendTo(card)

        return card
    }

    // Create Concrete Card
    function createCard(card_header, card_header_id, card_block, card_block_id) {
        let card = $(`
            <div class="card">
              <div class="card-header" role="tab" id="${card_header_id}">
                ${card_header}
              </div>

              <div id="${card_block_id}" class="collapse" role="tabpanel" aria-labelledby="heading${cbc["id"]}">
                <div class="card-block">
                  ${card_block}
                </div>
              </div>
            </div>
          `)

        return card
    }


    // Create Modal for Confirm Delete CBC Process
    function createModalToConfirmCBCDelete(analysis_id) {
        let modal_header = `
            <h5 class="modal-title" id="confirm_cbc${analysis_id}_modal_title">Delete CBC Analysis</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
        `

        let modal_body = `
            <div id="confirm_delete_cbc_error" class="row"></div>
            <p>Are you sure?.</p>
        `

        let modal_footer = `
            <button id="confirm_delete_cbc_button" type="submit" name="confirm" class="btn btn-outline-danger btn-block" data-cbc-id="${analysis_id}">Confirm</button>
            <button type="button" name="cancel" class="btn btn-outline-info btn-block" data-dismiss="modal">Cancel</button>
        `

        let confirm_delete_cbc_modal = createModal(`confirm_delete_cbc${analysis_id}_modal`, modal_header, modal_body, modal_footer)
        return confirm_delete_cbc_modal
    }

    // Create Modal for Add CBC Process
    function createModalToAddCBC(patient_id) {
        let modal_header = `
            <h5 class="modal-title" id="add_cbc_modal_title">Add CBC Analysis</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        `

        let modal_body = `
            <div id="add_cbc_error" class='row'></div>

            <form id="add_cbc_form" action="/patients/${patient_id}/analyzes/cbc/new" method="POST">
                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="WCB">WCB</label>
                  <div class="col-6">
                    <input class="form-control" id="WCB" name="WCB" placeholder="White Blod Cells" type="text" >
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="HGB">HGB</label>
                  <div class="col-6">
                    <input class="form-control" id="HGB" name="HGB" placeholder="Hemoglibin" type="text">
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="MCV">MCV</label>
                  <div class="col-6">
                    <input class="form-control" id="MCV" name="MCV" placeholder="Mean Corpuscular Volume" type="text" >
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="MCH">MCH</label>
                  <div class="col-6">
                    <input class="form-control" id="MCH" name="MCH" placeholder="Mean Cell Hemoglubine" type="text" >
                  </div>
                </div>

        </form>
        `

        let modal_footer = `
            <button id="add_cbc_button" type="submit" name="add" class="btn btn-outline-primary btn-block">Add</button>
            <button type="button" name="cancel" class="btn btn-outline-info btn-block" data-dismiss="modal">Cancel</button>
        `

        let add_cbc_modal = createModal("add_cbc_modal", modal_header, modal_body, modal_footer);

        return add_cbc_modal
    }

    // Create Modal for CBC Edit Process
    function createModalWithEditCBCForm(patient_id, analysis_type, analysis_data) {
        let modal_header = `
            <h5 class="modal-title" id="edit_cbc_modal_title">Edit CBC Analysis</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">×</span>
            </button>
        `

        let modal_body = `
            <div id="edit_cbc_error" class="row"></div>

            <form id="edit_cbc_form"
              action="/patients/${patient_id}/analyzes/${analysis_type}/edit/${analysis_data["id"]}"
              method="POST">
                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="WCB">WCB</label>
                  <div class="col-6">
                    <input class="form-control" id="WCB" name="WCB" placeholder="White Blod Cells" type="text" value="${analysis_data.wcb}">
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="HGB">HGB</label>
                  <div class="col-6">
                    <input class="form-control" id="HGB" name="HGB" placeholder="Hemoglibin" type="text" value="${analysis_data.hgb}">
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="MCV">MCV</label>
                  <div class="col-6">
                    <input class="form-control" id="MCV" name="MCV" placeholder="Mean Corpuscular Volume" type="text" value="${analysis_data.mcv}">
                  </div>
                </div>

                <div class="form-group row">
                  <label class="offset-2 col-2 col-form-label" for="MCH">MCH</label>
                  <div class="col-6">
                    <input class="form-control" id="MCH" name="MCH" placeholder="Mean Cell Hemoglubine" type="text" value="${analysis_data.mch}">
                  </div>
                </div>

            </form>
        `

        let modal_footer = `
            <button data-button-type="save" type="submit" name="save" class="btn btn-outline-primary btn-block">Save</button>
            <button id="cancel_save_cbc_button" type="button" name="cancel" data-dismiss="modal" class="btn btn-outline-info btn-block">Cancel</button>
        `

        let edit_cbc_modal = createModal("edit_cbc_modal", modal_header, modal_body, modal_footer)

        return edit_cbc_modal;
    }

    // Create Concrete Modal
    function createModal(modal_id, modal_header, modal_body, modal_footer) {
      let modal =  $(`
        <div id="${modal_id}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="${modal_id}_title" aria-hidden="true">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                ${modal_header}
              </div>

              <div class="modal-body">
                ${modal_body}
              </div>

              <div class="modal-footer">
                ${modal_footer}
              </div>
            </div>
          </div>
        </div>
      `)

      return modal
    }
  // }
})

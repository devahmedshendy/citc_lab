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
      "comment" : "",
      "comment_doctor": "",
      "approved": false,
    }

    var patient_id = $("#patient_personal_details").attr("data-patient-id");

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
    $(document).on('click', "[data-show-data-link]", (event) => {
        var edit_comment_link = $(event.target);

        console.log($(edit_comment_link)[0]);
        setGlobalCBC(...getCBCDataFromLink(edit_comment_link))

        console.log(cbc);

        var edit_comment_modal = createModalToShowData(patient_id, "cbc", cbc)
        $(edit_comment_modal).modal('show');
    });

    $(document).on('click', '#approve_comment_button', (event) => {
      var edit_comment_modal = $(event.target).closest('.modal');
      var action_url = $("#edit_comment_form").attr("action");

      var comment = JSON.stringify({
        "comment": $("#comment").val(),
      })

      $.ajax({
        method: "POST",
        url: action_url,
        contentType: 'application/json',
        data: comment
      })
      .done((messages) => {
          messages = JSON.parse(messages);

          if (messages.hasOwnProperty("error")) {
            let errors_list = messages["error"];

            clearAlert("#add_cbc_success");
            showErrorAlert("#edit_comment_error", errors_list);

          } else if (messages.hasOwnProperty("success")) {
            $(edit_comment_modal).modal('hide');

            let success_message = messages["success"];
            showSuccessAlert("#add_cbc_success", success_message);

          }
      })
      .fail((err) => {
          console.log(err);
      });
    });


    $(document).on('hidden.bs.modal', '#edit_comment_modal', (event) => {
      $(event.target).remove();
    });

    //-----------------------------------------
    //
    // Analysis Profile Page Functions
    //-----------------------------------------
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
                      $(link).attr("data-cbc-comment"),
                      $(link).attr("data-cbc-comment-doctor"),
                      $(link).attr("data-cbc-approved"), ];

        return cbc_data;
    }

    function setGlobalCBC(id, wcb, hgb, wcv, wch, comment, comment_doctor, approved) {
        cbc = { "id"      : id,                   "wcb"     : wcb,
                "hgb"     : hgb,                  "mcv"     : wcv,
                "mch"     : wch,                  "comment" : comment,
                "comment_doctor": comment_doctor, "approved": (approved == "true"), }
    }

    function resetGlobalCBC() {
        cbc = { "id"      : 0,        "wcb"     : 0,
                "hgb"     : 0,        "mcv"     : 0,
                "mch"     : 0,        "comment" : '',
                "comment_doctor": '', "approved": false, }
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
        let card_header = `
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">
                CBC Analysis - <small>${analysis_data["id"]}</small>
              </h6>
              <small>${analysis_data["updated_at"]}</small>
            </div>

            <div class="d-flex w-100 justify-content-between">
              <a href="#collapse${analysis_data["id"]}" data-toggle="collapse" data-parent="#accordion" aria-expanded="true" aria-controls="collapse${analysis_data["id"]}" class="flex-column align-items-start btn btn-link btn-sm">
                Show Data
              </a>

              <a href="/analyzes/patient_id/${patient_id}/cbc_id/${analysis_data["id"]}"
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
                        data-target="#edit_cbc_modal">Edit</a>
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
                        data-target="#confirm_delete_cbc${analysis_data["id"]}_modal">Delete</a>
                  </div>
                </div>
              </div>

              <div class="col-12">
                <hr>
                <div class="mb-1">
                  <h6 data-cbc-doctor class="text-muted">Confirmed by Dr.Zizo.</h6>
                    <p>
                      <span data-cbc-comment>${analysis_data["comment"]}</span>
                    </p>
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

    function createModalToShowData(patient_id, analysis_type, analysis_data) {
        var comment_element = ''

        if (analysis_data["approved"] == false) {
            comment_element = `
              <p class="text-muted">Not Approved Yet.</p>
            `

        } else if (analysis_data["approved"] == true){
            comment_element = `
              <p data-cbc-doctor-name class="text-muted">Approved By Dr. <span style="font-weight: bold">${analysis_data["comment_doctor"]}</span>.</p>
              <p class='form-control-static'>
                <span id="cbc${analysis_data["id"]}_comment">${analysis_data["comment"]}</span>
              </p>
            `
        }

        let modal_header = `
            <h5 class="modal-title" id="edit_comment_modal_title">Analysis Data</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        `

        let modal_body = `
            <div class="form-group row">
              <div class="offset-1 col-10">
                ${comment_element}
              </div>
            </div>

            <div class='row'>
                <div class='offset-1 col-10'>
                    <table class='table'>
                      <thead>
                        <tr>
                          <th>Item</th>
                          <th>Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <th scope="row">WCB</th>
                          <td>${analysis_data["wcb"]}</td>
                        </tr>

                        <tr>
                          <th scope="row">HGB</th>
                          <td>${analysis_data["hgb"]}</td>

                        <tr>
                          <th scope="row">MCV</th>
                          <td>${analysis_data["mcv"]}</td>
                        </tr>

                        <tr>
                          <th scope="row">MCH</th>
                          <td>${analysis_data["mch"]}</td>
                        </tr>
                      </tbody>
                    </table>
                </div>
            </div>
        `

        let modal_footer = `
            <a href="" name="cancel" class="btn btn-info btn-block" data-dismiss="modal">Cancel</a>
        `

        let edit_comment_modal = createModal("edit_comment_modal", modal_header, modal_body, modal_footer);

        return edit_comment_modal
    }

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
})

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
    displayCBCAnalyzesElements();

    $('#patient_analyzes_list').slimScroll({
        wheelStep: 3,
        alwaysVisible: true,
        railVisible: true,
        height: '400px',
    });


    $(document).on('click', "[data-edit-comment-link]", (event) => {
        var edit_comment_link = $(event.target);

        setGlobalCBC(...getCBCDataFromLink(edit_comment_link))

        var edit_comment_modal = createModalToEditComment(patient_id, "cbc", cbc)
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

            clearAlert("#cbc_success");
            showErrorAlert("#edit_comment_error", errors_list);

          } else if (messages.hasOwnProperty("success")) {
            $(edit_comment_modal).modal('hide');

            displayCBCAnalyzesElements();

            let success_message = messages["success"];
            showSuccessAlert("#cbc_success", success_message);

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

    function changeCBCCardComment(comment) {
        console.log(comment);
        console.log($(`#cbc${cbc["id"]}_comment`)[0]);
        $(`span#cbc${cbc["id"]}_comment`).text(comment["comment"]);
        // console.log($(`p span[data-cbc-comment]`)[0]);
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


    // Error/Success Alert Functions
    function showErrorAlert(alert_id, errors_list) {
      var error_alert = createErrorAlert(errors_list);
      $(alert_id).html(error_alert);
    }

    function showSuccessAlert(alert_id, success_message) {
      var success_element = createSuccessAlert(success_message);
      $(alert_id).html($(success_element));
    }

    function createErrorAlert(errors_list) {
        var ul_of_errors    = $(`<ul></ul>`);

        errors_list.forEach((message) => {
            let li = $(`<li>${message}</li>`).appendTo(ul_of_errors);
        });

        var error_alert = createAlert("error", ul_of_errors);
        return error_alert;
    }

    function createSuccessAlert(success_message) {
        var success_message = $(`<p>${success_message}</p>`)

        var success_alert = createAlert("success", success_message)
        return success_alert;
    }

    function clearAlert(alert_id) {
      $(alert_id).html('');
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


    // CBC Card Functions
    function createCBCCard(patient_id, analysis_type, analysis_data) {
        var comment_element = ''
        var approved_element = ''

        if (analysis_data["approved"] == false) {
            comment_element = `
              <p class="text-muted">Not Approved Yet.</p>
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

              <a href="/analyzes/patient_id/${patient_id}/cbc_id/${analysis_data["id"]}"
                  class="mb-1 btn btn-link btn-sm"
                  target="_blank"
                  data-print-pdf-link="print_pdf">PDF
              </a>
            </div>
        `


        let card_block = `
            <div class="row">
              <div class="container">
                <div class="row">
                  <div id="cbc_edit_options" class="col align-self-center text-center">
                    <a href="#"
                        data-edit-comment-link
                        data-cbc-id="${analysis_data["id"]}"
                        data-cbc-comment="${analysis_data["comment"]}"
                        data-cbc-wcb="${analysis_data["WCB"]}"
                        data-cbc-hgb="${analysis_data["HGB"]}"
                        data-cbc-mcv="${analysis_data["MCV"]}"
                        data-cbc-mch="${analysis_data["MCH"]}"
                        data-toggle="modal"
                        data-target="#edit_comment_modal">Edit Comment</a>
                  </div>
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

        return card
    }

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

    function createModalToEditComment(patient_id, analysis_type, analysis_data) {
      console.log(analysis_data);
        let modal_header = `
            <h5 class="modal-title" id="edit_comment_modal_title">Edit Comment</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        `

        let modal_body = `
            <div id="edit_comment_error" class='row'></div>

            <form id="edit_comment_form" action="/analyzes/cbc/${analysis_data["id"]}/approve" method="POST">
                <div class="form-group row">
                  <label class="col-12 col-form-label text-center" for="comment">Comment</label>
                  <div class="offset-1 col-10">
                    <textarea class="form-control" id="comment" name="comment" placeholder="Doctor comments..." rows="3"></textarea>
                  </div>
                </div>
            </form>

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
            <button type="button" name="cancel" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button id="approve_comment_button" type="submit" name="approve" class="btn btn-primary">Approve</button>
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

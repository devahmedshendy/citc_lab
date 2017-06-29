$(document).ready(() => {
  // === Analysis Profile Page ===============================================
  // if (page_name === "Analysis Profile") {

    var cbc = {
      "id"      : 0,
      "wcb"     : 0,
      "hgb"     : 0,
      "mcv"     : 0,
      "mch"     : 0,
      "comment" : "---",
    }

    // === Analysis Profile Initialization ====
    let patient_id = $("#patient_personal_details").attr("data-patient-id");
    $.get(`/patients/${patient_id}/analyzes?json=True`, (res) => {
        res = JSON.parse(res);

        displayCBCAnalyzesElements(patient_id, res);
    })
    .fail((err) => {
        console.log(err);
    });

    $('#patient_analyzes_list').slimScroll({
        wheelStep: 3,
        alwaysVisible: true,
        railVisible: true,
        height: '400px',
    });

    // === Analysis Profile Event Handlers ====
    // CBC Add Button Clicked
    $("#add_cbc_button").click((event) => {
        $("#add_cbc_form").submit();
    });


    // CBC Add Form Button Clicked
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
                let errors_list  = data["error"]
                let cbc_error_element = get_cbc_error_element(errors_list)

                $('#cbc_success').html('');
                $('#add_cbc_error').html($(cbc_error_element));

            } else if (data.hasOwnProperty("success")) {
                $("#add_cbc_form")[0].reset();
                $("#cbcModal").modal("hide");

                let success_message = data["success"]
                let success_col   = get_cbc_success_element(success_message);

                $('#add_cbc_error').html('');
                $('#cbc_success').html($(success_col));

                $.get(`/patients/${patient_id}/analyzes?json=True`, (res) => {
                    res = JSON.parse(res)

                    displayCBCAnalyzesElements(patient_id, res)
                })
                .fail((err) => {
                    console.log(err);
                });
            }
        });
    });



    // CBC Edit Button Clicked
    $(document).on('click', '[data-cbc-options-link=edit]', (event) => {
        var edit_cbc_link = $(event.target)

        set_global_cbc(...get_cbc_from_edit_link(edit_cbc_link))

        var edit_cbc_modal = get_edit_cbc_modal(cbc.id, cbc.comment,
                                                cbc.wcb, cbc.hgb,
                                                cbc.mcv, cbc.mch)

        $(edit_cbc_modal).modal('toggle');
    });


    // CBC Edit Form Cancel Button Clicked
    $(document).on('hidden.bs.modal', '#edit_cbc_modal', (event) => {
      var edit_cbc_modal = $(event.target)

      $(edit_cbc_modal).modal('hide');
      $(edit_cbc_modal).remove();

      reset_global_cbc();
    })


    // CBC Edit Form Save Button Clicked
    $(document).on('click', "[data-button-type=save]", (event)=> {
      $("#edit_cbc_form").submit()
    });


    // CBC Edit Form Submitted
    $(document).on('submit', "#edit_cbc_form", (event) => {
        event.preventDefault();

        var edit_cbc_form  = $(event.target)
        var action_url = edit_cbc_form.attr("action");
        cbc.id         = action_url.slice(-2);

        var edit_cbc_link = $(`#collapse${cbc.id} [data-cbc-options-link=edit]`);

        set_global_cbc(id = cbc.id, ...get_cbc_from_edit_form(edit_cbc_form));

        var submitted_data = JSON.stringify({
            "comment" : cbc.comment,
            "WCB"     : cbc.wcb,
            "HGB"     : cbc.hgb,
            "MCV"     : cbc.mcv,
            "MCH"     : cbc.mch
        })

        // POST CBC Data to the server
        $.ajax({
          method: 'POST',
          url: action_url,
          contentType: 'application/json',
          data: submitted_data
        })
        .done((messages) => {
            messages = JSON.parse(messages);

            if (messages.hasOwnProperty("error")) {
                let errors_list = messages["error"]
                let error_element = get_cbc_error_element(errors_list)

                $('#cbc_success').html('');
                $('#edit_cbc_error').html($(error_element));

            } else if (messages.hasOwnProperty("success")) {
                submitted_data = JSON.parse(submitted_data)

                var edit_cbc_link = $(`#collapse${cbc.id} [data-cbc-options-link=edit]`);
                var cbc_table     = $(`#table-${cbc.id}`)

                var cbc_comment   = $(`#collapse${cbc.id} span[data-cbc-comment]`)
                                      .text(submitted_data["comment"]);

                for (key in submitted_data) {
                  let data_element = `data-cbc-${key.toLowerCase()}`

                  $(edit_cbc_link).attr(`${data_element}`, submitted_data[key])

                  $(cbc_table).find(`[${data_element}]`)
                              .text(submitted_data[key])
                              .attr(`${data_element}`, submitted_data[key])
                }

                $('#edit_cbc_error').html('');
                $(edit_cbc_modal).modal('hide');

                let success_message = messages['success']
                let success_element = get_cbc_success_element(success_message)

                $('#cbc_success').html($(success_element));
            }
        })
        .fail((err) => {
            console.log(err);

        });

    });


    // === Analysis Profile Page Functions ====
    function get_cbc_from_edit_link(edit_cbc_link) {
      return [
        edit_cbc_link.attr("data-cbc-id"),
        edit_cbc_link.attr("data-cbc-wcb"),
        edit_cbc_link.attr("data-cbc-hgb"),
        edit_cbc_link.attr("data-cbc-mcv"),
        edit_cbc_link.attr("data-cbc-mch"),
        edit_cbc_link.attr("data-cbc-comment")
      ];
    }

    function get_cbc_from_edit_form(edit_cbc_form) {
      return [
        $("#edit_cbc_form #WCB").val(),
        $("#edit_cbc_form #HGB").val(),
        $("#edit_cbc_form #MCV").val(),
        $("#edit_cbc_form #MCH").val(),
        $("#edit_cbc_form #comment").val()
      ];
    }


    function set_global_cbc(id, wcb, hgb, wcv, wch, comment) {
      cbc = {
        "id"      : id      ? id      : cbc.id,
        "wcb"     : wcb     ? wcb     : cbc.wcb,
        "hgb"     : hgb     ? hgb     : cbc.hgb,
        "mcv"     : wcv     ? wcv     : cbc.mcv,
        "mch"     : wch     ? wch     : cbc.mch,
        "comment" : comment ? comment : cbc.comment,
      }
    }

    function reset_global_cbc() {
      cbc = {
        "id"      : 0,
        "wcb"     : 0,
        "hgb"     : 0,
        "mcv"     : 0,
        "mch"     : 0,
        "comment" : "---",
      }
    }


    function get_cbc_success_element(success_message='') {
      return $(`
          <div class='offset-3 col-6'>
              <div class='alert alert-success alert-dismissible fade show' role='alert'>
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                  </button>
                  ${success_message}
              </div>
          </div>
      `);
    }

    function get_cbc_error_element(errors_list={}) {
      /*
      <div class="offset-3 col-6">
        <div class="alert alert-danger" role="alert">
          <ul>
              <li>error</li>
          </ul>
        </div>
      </div>
      */
      let error_col   = $(`<div class='offset-1 col-10'></div>`);
      let alert = $(`<div class='alert alert-danger' role='alert'></div>`).appendTo(error_col);
      let ul    = $(`<ul></ul>`).appendTo(alert)

      errors_list.forEach((message) => {
          let li = $(`<li>${message}</li>`).appendTo(ul);
      });

      return error_col;
    }

    function displayCBCAnalyzesElements(patient_id='', cbc_analyzes={}) {
        var accordion = $("#patient_analyzes_list #accordion")
                        .first()
                        .html('')

        cbc_analyzes.forEach((cbc) => {
            cbc["patient_id"] = patient_id
            get_cbc_card(cbc).appendTo(accordion)
        });
    }

    function get_cbc_card(cbc={}) {
      return $(`
          <div class="card">
            <div class="card-header" role="tab" id="heading${cbc['id']}">
              <div>
              <div class="d-flex w-100 justify-content-between">
                <!-- "analysis_type": "CBC Analysis" -->
                <h6 class="mb-1">
                  CBC Analysis - <small>${cbc['id']}</small>
                </h6>

                <!-- "created_at": "2017-05-29" -->
                <small>${cbc['updated_at']}</small>
              </div>

              <div class="d-flex w-100 justify-content-between">
                <a href="#collapse${cbc['id']}" data-toggle="collapse" data-parent="#accordion" aria-expanded="true" aria-controls="collapse${cbc['id']}" class="flex-column align-items-start btn btn-link btn-sm">
                  Display Result
                </a>

                <a href="/analyzes/patient_id/${cbc["patient_id"]}/cbc_id/${cbc["id"]}"
                    class="mb-1 btn btn-link btn-sm"
                    target="_blank"
                    data-cbc-options-link="print_pdf">PDF
                </a>
              </div>
              </div>
            </div>

            <div id="collapse${cbc["id"]}" class="collapse" role="tabpanel" aria-labelledby="heading${cbc["id"]}">
              <div class="card-block">
                <div class="row">
                  <div class="container">
                    <div class="row">
                      <div id="cbc_edit_options" class="col align-self-center text-center">
                        <a href="#"
                            data-cbc-options-link="edit"
                            data-cbc-id="${cbc["id"]}"
                            data-cbc-comment="${cbc["comment"]}"
                            data-cbc-wcb="${cbc["WCB"]}"
                            data-cbc-hgb="${cbc["HGB"]}"
                            data-cbc-mcv="${cbc["MCV"]}"
                            data-cbc-mch="${cbc["MCH"]}"
                            data-toggle="modal"
                            data-target="#edit_cbc_modal">Edit</a>
                        |
                        <a href="#"
                            data-cbc-id="${cbc["id"]}"
                            data-cbc-comment="${cbc["comment"]}"
                            data-cbc-wcb="${cbc["WCB"]}"
                            data-cbc-hgb="${cbc["HGB"]}"
                            data-cbc-mcv="${cbc["MCV"]}"
                            data-cbc-mch="${cbc["MCH"]}"
                            data-toggle="modal"
                            data-target="#delete_cbc${cbc["id"]}_confirmation">Delete</a>
                      </div>
                    </div>
                  </div>

                  <div class="col-12">
                    <hr>
                    <div class="mb-1">
                      <h6 data-cbc-doctor class="text-muted">Confirmed by Dr.Zizo.</h6>
                        <p>
                          <span data-cbc-comment>${cbc["comment"]}</span>
                        </p>
                    </div>

                    <table id="table-${cbc["id"]}" class="table table-sm">
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
                          <td data-cbc-wcb=${cbc["WCB"]}>${cbc["WCB"]}</td>
                          <td>3.70 - 10.10</td>
                        </tr>
                        <tr>
                          <th scope="row">HGB</th>
                          <!-- "HGB": "12.9" -->
                          <td data-cbc-hgb=${cbc["HGB"]}>${cbc["HGB"]}</td>
                          <td>12.9 - 15.9</td>
                        </tr>
                        <tr>
                          <th scope="row">MCV</th>
                          <!-- "MCV": "82.2" -->
                          <td data-cbc-mcv=${cbc["MCV"]}>${cbc["MCV"]}</td>
                          <td>81.1 - 96.0</td>
                        </tr>
                        <tr>
                          <th scope="row">MCH</th>
                          <!-- "MCH": "27.3" -->
                          <td data-cbc-mch=${cbc["MCH"]}>${cbc["MCH"]}</td>
                          <td>27.0 - 31.2</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="row">
            <div id="delete_cbc${cbc["id"]}_confirmation" class="modal fade">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Delete CBC Analysis</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    <p>Are you sure?.</p>
                  </div>
                  <form action="/analyzes/cbc_analyzes/personal_id/${patient_id}/cbc_id/${cbc['id']}" method="GET">
                    <div class="modal-footer">
                      <button type="submit" class="btn btn-danger">Yes, Sure</button>
                      <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

        `)
    }

    function get_edit_cbc_modal(cbc_id='', cbc_comment='', cbc_wcb='',
                                cbc_hgb='', cbc_mcv='', cbc_mch='') {
        return $(`
            <div class="modal fade" id="edit_cbc_modal" tabindex="-1" role="dialog" aria-labelledby="edit_cbc_modal_title" aria-hidden="true">
                <div class="modal-dialog" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="edit_cbc_modal_title">Edit CBC Analysis</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                      </button>
                    </div>

                    <div class="modal-body">
                        <div id="edit_cbc_error" class="row"></div>

                        <form id="edit_cbc_form"
                          action="/analyzes/patient_id/26011231201016/cbc_id/${cbc_id}"
                          method="POST">

                            <div class="form-group row">
                              <label class="col-12 col-form-label text-center" for="comment">Comment</label>
                              <div class="offset-1 col-10">
                                <textarea class="form-control" id="comment" name="comment" placeholder="Doctor comments..." rows="3">${cbc_comment === '---' ? '' : cbc_comment}</textarea>
                              </div>
                            </div>

                            <div class="form-group row">
                              <label class="offset-2 col-2 col-form-label" for="WCB">WCB</label>
                              <div class="col-6">
                                <input class="form-control" id="WCB" name="WCB" placeholder="White Blod Cells" type="text" value="${cbc_wcb}">
                              </div>
                            </div>

                            <div class="form-group row">
                              <label class="offset-2 col-2 col-form-label" for="HGB">HGB</label>
                              <div class="col-6">
                                <input class="form-control" id="HGB" name="HGB" placeholder="Hemoglibin" type="text" value="${cbc_hgb}">
                              </div>
                            </div>

                            <div class="form-group row">
                              <label class="offset-2 col-2 col-form-label" for="MCV">MCV</label>
                              <div class="col-6">
                                <input class="form-control" id="MCV" name="MCV" placeholder="Mean Corpuscular Volume" type="text" value="${cbc_mcv}">
                              </div>
                            </div>

                            <div class="form-group row">
                              <label class="offset-2 col-2 col-form-label" for="MCH">MCH</label>
                              <div class="col-6">
                                <input class="form-control" id="MCH" name="MCH" placeholder="Mean Cell Hemoglubine" type="text" value="${cbc_mch}">
                              </div>
                            </div>

                        </form>

                    </div>
                    <div class="modal-footer">
                      <button id="cancel_save_cbc_button" type="button" name="cancel" data-dismiss="modal" class="btn btn-secondary">Cancel</button>
                      <button data-button-type="save" type="submit" name="save" class="btn btn-primary">Save</button>
                    </div>
                  </div>
                </div>
              </div>
        `)
    }
  // }
})

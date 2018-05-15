"use strict";

// Don't cache ajax requests
$.ajaxSetup({cache: false});

$(function () {
    $("[data-toggle='popover']").popover();
});

$(function () {
    $(".disable-enter-submit").keypress(function (e) {
        if (e.keyCode === "13") {
            e.preventDefault();
        }
    });
});

function characterCounter(target, limit, currentLength, minLength) {
    /* Global character counter
     *
     * Parameters:
     * - target: string of target selector
     * - limit: integer of maximum character length
     * - currentLength: integer value of keyed in content
     * - minLength: integer of minimum character length (default = 0)
     *
     * Ex:
     * {
     *     target: "#note-content",
     *     charLength: 500,
     *     contentLength: $(this).val().length,
     *     minLength: 0
     * }
     *
     * */
    var length = limit - currentLength;
    minLength = (typeof minLength !== "undefined") ? minLength : 0;
    var s = length === 1 ? "" : "s";
    $(target).text(length + " character" + s + " remaining");
    if (length == 0) {
        $(target).css("color", "red");
    } else if (currentLength < minLength) {
        $(target).css("color", "red");
    }
    else {
        $(target).css("color", "black");
    }
}

function regexUrlChecker(value) {
    /* Global regexUrlChecker
     *
     * Checks the value of a url link using regex with one of the following allowed protocols: http, https, ftp, git
     *
     * Parameters:
     * value: string of link url
     *
     * Returns: does value match regex object?
     * */
    var regex = /^(https?|s?ftp|git):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;
    return regex.test(value);
}

/* jquery datepicker */

// An array of holiday dates to be disabled
var holiday_dates = null;

function notHolidayOrWeekend(date, forPicker) {
    /* Global notHolidayOrWeekend
     *
     * http://api.jqueryui.com/datepicker/#option-beforeShowDay
     *
     * WARNING:
     * --------
     * 'holiday_dates' must be set globally before calling this function.
     */
    if (typeof(forPicker) === "undefined") {
        forPicker = true;
    }
    var formattedDate = $.datepicker.formatDate("yy-mm-dd", date);
    var holiday_or_weekend = $.inArray(formattedDate, holiday_dates) !== -1 ||
        date.getDay() === 0 || date.getDay() === 6;
    // TODO: would be nice to display the name of the holiday (tooltip)
    return forPicker ? [!holiday_or_weekend] : !holiday_or_weekend;
}

function getRequestAgencyInstructions() {
    /* Global getAgencyInstructions
     *
     * ajax call to get additional information for the specified agency
     */
    var agencyEin = $("#request-agency").val();
    var requestInstructionsDiv = $("#request-agency-instructions");
    var requestInstructionsContentDiv = $("#request-agency-instructions-content");

    if (agencyEin !== "") {
        $.ajax({
            url: "/agency/feature/" + agencyEin + "/" + "specific_request_instructions",
            type: "GET",
            success: function (data) {
                if (data["specific_request_instructions"]["text"] !== "") {
                    requestInstructionsContentDiv.html("<p>" + data["specific_request_instructions"]["text"] + "</p>");
                    requestInstructionsDiv.show();
                }
                else {
                    requestInstructionsDiv.hide();
                }
            },
            error: function () {
                requestInstructionsDiv.hide();
            }
        });
    }
}

function toggleRequestAgencyInstructions(action) {
    /* Global toggleRequestAgencyInstructions
     *
     * determine whether or not to show agency instruction content
     */
    var el = $("#request-agency-instructions-toggle");
    var requestInstructionsContentDiv = $("#request-agency-instructions-content");
    var hideHtml = "<button type=\"button\" id=\"request-agency-instructions-btn\" class=\"btn btn-block btn-info\"><span class=\"glyphicon glyphicon-chevron-up\"></span>&nbsp;&nbsp;Hide Agency Instructions&nbsp;&nbsp;<span class=\"glyphicon glyphicon-chevron-up\"></span></button>";
    var showHtml = "<button type=\"button\" id=\"request-agency-instructions-btn\" class=\"btn btn-block btn-info\"><span class=\"glyphicon glyphicon-chevron-down\"></span>&nbsp;&nbsp;Show Agency Instructions&nbsp;&nbsp;<span class=\"glyphicon glyphicon-chevron-down\"></span></button>";

    if (action === "show") {
        el.html(hideHtml);
        requestInstructionsContentDiv.show();
    }
    else if (action === "hide") {
        el.html(showHtml);
        requestInstructionsContentDiv.hide();
    }
    else if (action === "default") {
        if (el.html() === showHtml) {
            el.html(hideHtml);
            requestInstructionsContentDiv.show();
        } else {
            el.html(showHtml);
            requestInstructionsContentDiv.hide();
        }
    }
}

var showMultipleRequestTypes = false;
var repeatableCounter = {};
var customRequestFormCounter = 1;
function getCustomRequestForms(agencyEin) {
    /* exported getCustomRequestForms
     *
     * function to determine if custom request forms need to be shown on category or agency change
     */
    var selectedAgency = agencyEin;
    var customRequestFormsDivId = "#custom-request-forms-" + customRequestFormCounter.toString();
    var requestTypeId = "#request-type-" + customRequestFormCounter.toString();
    var customRequestFormId = "#custom-request-form-content-" + customRequestFormCounter.toString();
    var customRequestFormsDiv = $(customRequestFormsDivId);
    var requestType = $(requestTypeId);
    var customRequestFormContent = $(customRequestFormId);
    var customRequestFormAdditionalContent = $("#custom-request-form-additional-content");

    requestType.empty();
    customRequestFormContent.html("");
    customRequestFormContent.hide();
    customRequestFormAdditionalContent.hide();
    // ajax call to show request type drop down
    $.ajax({
        url: "/agency/feature/" + selectedAgency + "/" + "custom_request_forms",
        type: "GET",
        success: function (data) {
            if (data["custom_request_forms"]["enabled"] === true) {
                // ajax call to populate request type drop down with custom request form options
                $.ajax({
                    url: "/agency/api/v1.0/custom_request_forms/" + selectedAgency,
                    type: "GET",
                    success: function (data) {
                        if (data.length === 1) {
                            requestType.append(new Option(data[0][1], data[0][0]));
                            customRequestFormsDiv.show();
                            renderCustomRequestForm();
                            // add repeatable form if only one form
                        }
                        else {
                            requestType.append(new Option("", ""));
                            for (var i = 0; i < data.length; i++) {
                                repeatableCounter[data[i][0]] = data[i][2]; // set the keys to be the form id
                                var option = new Option(data[i][1], data[i][0]);
                                if (repeatableCounter[data[i][0]] === 0){
                                    // disable it
                                    option.disabled = true;
                                }
                                requestType.append(option);
                            }
                            customRequestFormsDiv.show();
                        }
                    }
                });
                // check is custom forms are repeatable
                if (data["custom_request_forms"]["multiple_request_types"] === true) {
                    showMultipleRequestTypes = true;
                }
                else {
                    showMultipleRequestTypes = false;
                }
            }
            else {
                customRequestFormsDiv.hide();
            }
        },
        error: function () {
            customRequestFormsDiv.hide();
        }
    });
}

function populateDropdown(agencyEin) {
    var selectedAgency = agencyEin;
    $(".request-type").each(function(){
        if (this.length === 0) { // if this is an unpopulated dropdown
            var requestType = this;
            $.ajax({
                url: "/agency/api/v1.0/custom_request_forms/" + selectedAgency,
                type: "GET",
                success: function (data) {
                    // Still need to account for only 1 custom form

                    requestType.append(new Option("", ""));
                    for (var i = 0; i < data.length; i++) {
                        var option = new Option(data[i][1], data[i][0]);
                        if (repeatableCounter[data[i][0]] === 0) {
                            // disable it
                            option.disabled = true;
                        }
                        requestType.append(option);
                    }
                }
            });
        }
    });
}

var previousFormId = "";
var formCurrentlyDisplayed = false;
function renderCustomRequestForm(target) {
    /*
     * function to render custom form fields based on their field definitions
     */
    var requestTypeId = "#request-type-" + target;
    var requestType = $(requestTypeId);
    var formId = $(requestType).val();
    var agencyEin = $("#request-agency").val();
    var customRequestFormId = "#custom-request-form-content-" + target;
    var customRequestFormContent = $(customRequestFormId);
    var customRequestFormAdditionalContent = $("#custom-request-form-additional-content");

    if (formId !== "") {
        $.ajax({
            url: "/agency/api/v1.0/custom_request_form_fields",
            type: "GET",
            data: {
                form_id: formId,
                agency_ein: agencyEin,
                repeatable_counter: JSON.stringify(repeatableCounter)
            },
            success: function (data) {
                // if (formCurrentlyDisplayed) {
                //     // repeatableCounter[previousFormId] = repeatableCounter[previousFormId] + 1;
                // }
                // formCurrentlyDisplayed = true;
                // previousFormId = formId;
                // repeatableCounter[formId] = repeatableCounter[formId] - 1;
                customRequestFormContent.html(data);
                // console.log(previousFormId);
                // console.log(repeatableCounter);

                // render datepicker plugins
                $(".custom-request-form-datepicker").datepicker({
                    dateFormat: "mm/dd/yy",
                    maxDate: 0
                }).keydown(function (e) {
                    // prevent keyboard input except for tab
                    if (e.keyCode !== 8 &&
                        e.keyCode !== 9 &&
                        e.keyCode !== 37 &&
                        e.keyCode !== 39 &&
                        e.keyCode !== 48 &&
                        e.keyCode !== 49 &&
                        e.keyCode !== 50 &&
                        e.keyCode !== 51 &&
                        e.keyCode !== 52 &&
                        e.keyCode !== 53 &&
                        e.keyCode !== 54 &&
                        e.keyCode !== 55 &&
                        e.keyCode !== 56 &&
                        e.keyCode !== 57 &&
                        e.keyCode !== 191)
                        e.preventDefault();
                });


                try {
                    // render timepicker plugins
                    $(".timepicker").timepicker({
                        timeFormat: "h:mm p",
                        interval: 1,
                        minTime: "12:00am",
                        maxTime: "11:59pm",
                        startTime: "12:00am",
                        dynamic: false,
                        dropdown: true,
                        scrollbar: true
                    }).keydown(function (e) {
                        // prevent keyboard input except for allowed keys
                        if (e.keyCode !== 8 &&
                            e.keyCode !== 9 &&
                            e.keyCode !== 37 &&
                            e.keyCode !== 39 &&
                            e.keyCode !== 48 &&
                            e.keyCode !== 49 &&
                            e.keyCode !== 50 &&
                            e.keyCode !== 51 &&
                            e.keyCode !== 52 &&
                            e.keyCode !== 53 &&
                            e.keyCode !== 54 &&
                            e.keyCode !== 55 &&
                            e.keyCode !== 56 &&
                            e.keyCode !== 57 &&
                            e.keyCode !== 16 &&
                            e.keyCode !== 65 &&
                            e.keyCode !== 77 &&
                            e.keyCode !== 80 &&
                            e.keyCode !== 186)
                            e.preventDefault();
                    });

                }
                catch (err) {
                    // One of the forms doesn't have a time field with will throw an error when you try to render it
                    // TODO: find a better way to handle this error
                }

                // Do not reset on click
                $(".select-multiple").find("option").mousedown(function (e) {
                    e.preventDefault();
                    $(".select-multiple").focus();
                    $(this).prop("selected", !$(this).prop("selected"));
                    return false;
                });

                customRequestFormContent.show();
                // check to show add new request information button
                if (showMultipleRequestTypes === true) {
                    customRequestFormAdditionalContent.show();
                }
                else {
                    customRequestFormAdditionalContent.hide();
                }
            }
        });
    }
    else {
        customRequestFormContent.html("");
        customRequestFormContent.hide();
        customRequestFormAdditionalContent.hide();
        // reset the repeatable counter for that formId
        // repeatableCounter[previousFormId] = repeatableCounter[previousFormId] + 1;
        // console.log(repeatableCounter);
    }
}
function buildSite(responseData) {
    $("#site-container").empty();
    $("#interface-container").empty();
    $("#site-insight-container").empty();

    $.each(responseData, function (index, data) {
        var $site = $("#site-template").clone();
        var $siteInsight = $("#site-insight").clone();
        var $model = $("#interface-modal").clone();

        var comment = data.comments || "No comment";

        var siteId = "site-" + data.name;
        // Site data
        $site.attr("id", siteId);
        $site.find("#ipsec-name").text(data.name);
        $site.find("#ipsec-comment").text(comment);

        var status = data.status;

        if (status.toLowerCase() == "up") {
            $site
                .find("#ipsec-status")
                .attr("class", "badge bg-success rounded-pill");
            $site.find("#ipsec-status").text(data.status);
        } else if (status.toLowerCase() == "down") {
            $site.find("#ipsec-status").attr("class", "badge bg-danger rounded-pill");
            $site.find("#ipsec-status").text(data.status);
        } else {
            $site
                .find("#ipsec-status")
                .attr("class", "badge bg-secondary rounded-pill");
            $site.find("#ipsec-status").text(data.status);
        }

        $site.find("#ipsec-ip").text(data.ip);
        $site.find("#ipsec-interface").text(data.interface);
        $site.find("#card-footer").text(data.serial_number);

        var siteInsightId = "site-insight" + data.name;
        $siteInsight.attr("id", siteInsightId);
        var siteInsightBtnId = "collapse-insight-btn" + data.name.toLowerCase();
        var siteInsightCollapseId = "collapse-insight-" + data.name.toLowerCase();

        $site
            .find("#site-insight-button")
            .attr("href", "#" + siteInsightCollapseId);
        $site.find("#site-insight-button").attr("id", siteInsightBtnId);
        $site
            .find("#site-insight-button")
            .attr("aria-controls", siteInsightCollapseId);
        $site.find("#ipsec-incoming-core").text(data.incoming_core);
        $site.find("#ipsec-outgoing-core").text(data.outgoing_core);
        $site.find("#ipsec-incoming-tunnel").text(data.incoming_tunnel);
        $site.find("#ipsec-outgoing-tunnel").text(data.outgoing_tunnel);

        $siteInsight
            .find("#site-insight-collapse")
            .attr("id", siteInsightCollapseId);

        // Site insight data
        $siteInsight.find("#ipsec-src1").text(data.src1);
        $siteInsight.find("#ipsec-src2").text(data.src2);
        $siteInsight.find("#ipsec-src3").text(data.src3);
        $siteInsight.find("#ipsec-src4").text(data.src4);

        $siteInsight.find("#ipsec-dst1").text(data.dst1);
        $siteInsight.find("#ipsec-dst2").text(data.dst2);

        $site.find("#site-insight-container").append($siteInsight);

        if (data.interface == "non") {
            $site.find("#launch-modal").hide();
        }

        // Site's Interface Switch Fields
        var to = "wan1";
        if (data.interface == "wan1") {
            to = "wan2";
        }

        var interface_modal_id = "interface-modal-" + data.name.toLowerCase();
        $site.find("#launch-modal").attr("href", "#" + interface_modal_id);

        var interface_modal_id = "interface-modal-" + data.name.toLowerCase();
        $model.attr("id", interface_modal_id);
        $model.find("#modal-title").text("Interface Switch for " + data.name);

        $model
            .find("#interface-desc")
            .text(
                "Are you sure you want switch " +
                comment +
                " from " +
                data.interface +
                " to " +
                to +
                "?"
            );
        $model.find("#input-name").attr("value", comment);
        $model.find("#input-abbr").attr("value", data.name);
        $model.find("#input-serial-number").attr("value", data.serial_number);
        $model.find("#input-interface").attr("value", data.interface);

        $site.removeAttr("hidden");

        $("#site-container").append($site);
        $("#modal-container").append($model);
    });
}

function buildUnavailableSite(responseData){
    $("#site-container").empty();
    $("#interface-container").empty();
    $("#site-insight-container").empty();

    $.each(responseData, function (index, data) {
        var $site = $("#unavailable-template").clone();

        console.log(data.serial_number);
        $site.find("#unavailable-title").text(data.site_tag + "is Currently Unavailable");
        $site.find('#unavailable-serial').text(data.serial_number);
        $site.find('#unavailable-tag').text(data.site_tag);
        $site.find('#unavailable-status').text(data.site_status);

        $site.removeAttr("hidden");

        $("#site-container").append($site);
    });    
}
function getUnavailableSites(backend_url, callback) {
    // Make Server-side AJAX GET
    $.ajax({
        url: backend_url,
        type: "GET",
        dataType: "json",
        success: function (responseData) {
            // Hide spinner on success and display data
            $("#spinner").hide();

            console.log(responseData.count);
            if (responseData.count == 0) {
                _toast = alertMsg(
                    "Retrieval Success!",
                    "All sites are currently available on the network.",
                    "info",
                    10000
                );
            } else {
                buildUnavailableSite(responseData);
                _toast = alertMsg(
                    "Retrieval Success!",
                    "Displaying currently unavailable network sites.",
                    "success",
                    10000
                );
            }

            _toast.show();
        },
        error: function () {
            // Handle errors
            _toast = alertMsg(
                "Have you tried turning it off & on?",
                "There was an exception thrown somewhere in the depths of the the source code. Try refreshing, logging out and back in to resolve. Alternatively contact Branden the Developer via email(branden-van-staden@outlook.com).",
                "error",
                60000
            );
            _toast.show();
        },
    });
}

function getAvailableSites(backend_url, callback) {
    // Make Server-side AJAX GET
    $.ajax({
        url: backend_url,
        type: "GET",
        dataType: "json",
        success: function (responseData) {
            // Hide spinner on success and display data
            $("#spinner").hide();

            console.log(responseData.count);
            if (responseData.count == 0) {
                _toast = alertMsg(
                    "Retrieval Success!",
                    "No sites with the selected filter.",
                    "info",
                    10000
                );
            } else {
                buildSite(responseData);
                _toast = alertMsg(
                    "Retrieval Success!",
                    "Displaying sites.",
                    "success",
                    10000
                );
            }

            _toast.show();
        },
        error: function () {
            // Handle errors
            _toast = alertMsg(
                "Whoops this is embarrassing.",
                "Internal Error, please contact brandenconnected@gmail.com if this persists!",
                "error",
                1000
            );
            _toast.show();
        },
    });
}

function searchSerialNumber(backend_url) {
    $.ajax({
        url: backend_url,
        type: "POST",
        dataType: "json",
        success: function (responseData) {
            $("#spinner").hide();

            _toast = alertMsg(
                "Retrieval Success!",
                "Displaying site...",
                "success",
                10000
            );
            _toast.show();

            var template = buildTemplate(responseData);
            return template;
        },
        error: function () {
            // Handle errors
            _toast = alertMsg(
                "Whoops this is embarrassing.",
                "Internal Error, please contact brandenconnected@gmail.com if this persists!",
                "error",
                1000
            );
            _toast.show();
        },
    });
}

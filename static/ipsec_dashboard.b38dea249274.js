function buildIPsecTemplate(responseData) {
    // Create an array to store the modified templates
    var modifiedTemplates = [];

    // Clone the template for each VPN tunnel
    var $template = $('#ipsec-template').clone();

    // Loop through the list of VPN tunnels
    $.each(responseData, function (index, data) {
        var comment = ' ';

        if (data.comments == '') {
            comment = '--';
        } else {
            comment = data.comments;
        }

        // IPsec Tunnel Data
        $template.find('#ipsec-name').text(data.name);// IPsec/VPN Tunnel Name
        $template.find('#ipsec-comment').text(comment); // IPsec/VPN Short Hand
        $template.find('#ipsec-status').text(data.status); // IPsec/VPN Tunnel Status
        $template.find('#ipsec-ip').text(data.ip); // IPsec/VPN Core IP
        $template.find('#ipsec-interface').text(data.interface); // IPsec/VPN Tunnel's Interface
        $template.find('#ipsec-incoming-core').text(data.incoming_core); // IPsec/VPN Core Incoming Traffic
        $template.find('#ipsec-outgoing-core').text(data.outgoing_core); // IPsec/VPN Core Name Outgoing Traffic
        $template.find('#ipsec-incoming-tunnel').text(data.incoming_tunnel); // IPsec/VPN Tunnel Incoming Traffic
        $template.find('#ipsec-outgoing-tunnel').text(data.outgoing_tunnel); // IPsec/VPN Tunnel Outgoing Traffic
        $template.find('#card-footer').text(data.username); // IPsec/VPN Tunnel Parent

        // IPsec Proxy Data - src
        $template.find('#ipsec-src1').text(data.src1);
        $template.find('#ipsec-src2').text(data.src2);
        $template.find('#ipsec-src3').text(data.src3);
        $template.find('#ipsec-src4').text(data.src4);

        // IPsec Proxy Data - dst
        $template.find('#ipsec-dst1').text(data.dst1);
        $template.find('#ipsec-dst2').text(data.dst2);

        // IPsec Interface Data
        $template.find('#ipsec-interface').text(data.interface);
        if (data.interface == 'none') {
            $template.find('#launch-modal').hide();
        }
        var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

        $template.find('#launch-modal').attr('href', '#' + interface_modal_id); 

        // Remove the hidden Attribute from Template
        $template.removeAttr('hidden');

        // Push the modified template to the array
        modifiedTemplates.push($template.clone());
    });

    // Return the array of modified templates
    return modifiedTemplates;
}

function buildInterfaceModel(modelData) {
    // Loop through the list of VPN tunnels
    $.each(responseData, function (index, data) {
        var $model = $('#interface-modal').clone();
        var interface_modal_id = 'interface-modal-' + data.name.toLowerCase();

        $model.attr('id', interface_modal_id);
        $model.find('#modal-title').text('Interface Switch for ' + data.name);

        var to = 'wan1';
        if (data.interface == 'wan1') {
            to = 'wan2'
        }
        $model.find('#interface-desc').text('Are you sure you want switch ' + comment + ' from ' + data.interface + ' to ' + to + '?');
        $model.find('#input-name').attr('value', comment);
        $model.find('#input-abbr').attr('value', data.name);
        $model.find('#input-serial-number').attr('value', data.serial_number);
        $model.find('#input-interface').attr('value', data.interface)
    });
}

function getAvailableSites(backend_url, callback) {
    // Make Server-side AJAX GET
    $.ajax({
        url: backend_url,
        type: 'GET',
        dataType: 'json',
        success: function (responseData) {
            // Hide spinner on success and display data
            $('#spinner').hide();

            // Call the callback function with the responseData
            callback(responseData);

            _toast = alertMsg('Retrieval Success!', 'Displaying working sites.', 'success', 10000);
            _toast.show();
        },
        error: function () {
            // Handle errors
            _toast = alertMsg('Whoops this is embarrassing.', 'Internal Error, please contact brandenconnected@gmail.com if this persists!', 'error', 1000)
            _toast.show();
        }
    });
}

function searchSerialNumber(backend_url) {
    $.ajax({
        url: backend_url,
        type: 'POST',
        dataType: 'json',
        success: function (responseData) {
            $('#spinner').hide();

            _toast = alertMsg('Retrieval Success!', 'Displaying site...', 'success', 10000);
            _toast.show();

            var template = buildTemplate(responseData);
            return template
        },
        error: function () {
            // Handle errors
            _toast = alertMsg('Whoops this is embarrassing.', 'Internal Error, please contact brandenconnected@gmail.com if this persists!', 'error', 1000)
            _toast.show();
        }
    });
}

